"""Agent class."""

import copy
import os
import sys
import time
import uuid
from collections import defaultdict
from pathlib import Path
from typing import Any, Literal

from schwarm.configs.telemetry_config import TelemetryConfig
from schwarm.core.logging import log_function_call, logger, setup_logging
from schwarm.core.tools import ToolHandler
from schwarm.events.event import EventType
from schwarm.models.agents.terminator import TerminatorAgent
from schwarm.models.agents.user_agent import UserAgent
from schwarm.models.event import create_event, create_full_event
from schwarm.models.message import Message
from schwarm.models.provider_context import ProviderContextModel
from schwarm.models.types import Agent, Response
from schwarm.provider.base.base_llm_provider import BaseLLMProviderConfig
from schwarm.provider.base.base_provider import BaseProviderConfig
from schwarm.provider.llm_provider import LLMProvider
from schwarm.provider.provider_manager import ProviderManager
from schwarm.telemetry.base.telemetry_exporter import TelemetryExporter
from schwarm.telemetry.sqlite_telemetry_exporter import SqliteTelemetryExporter
from schwarm.telemetry.telemetry_manager import TelemetryManager
from schwarm.utils.function import function_to_json
from schwarm.utils.settings import APP_SETTINGS

logger.add(
    f"{APP_SETTINGS.DATA_FOLDER}/logs/debug.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="10 MB",
)


class Schwarm:
    """Agent orchestrator class."""

    def __init__(
        self,
        agent_list: list[Agent] = [],
        telemetry_exporters: list[TelemetryExporter] = [SqliteTelemetryExporter()],
        application_mode: Literal["code", "server"] = "code",
    ):
        """Initialize the orchestrator."""
        logger.remove()
        self._default_handler = logger.add(sys.stderr, level="DEBUG")
        self._environment = self.get_environment()

        self._agents = agent_list
        self.telemetry_exporters = telemetry_exporters
        if telemetry_exporters:
            self._telemetry_manager = TelemetryManager(telemetry_exporters)
        self._provider_manager = ProviderManager(telemetry_manager=self._telemetry_manager)

        if application_mode == "server":
            self.run_server()

        # self._run_id = None
        # module = load_module("D:\\Projects\\_serious\\schwarm\\examples\\05_fakeuser_generator\\app.py")
        # objects = find_objects_of_type(module, Agent)

        # for name in objects:
        #     logger.info(f"Agent {name} loaded successfully.")

        # self.loaded_agents = objects

        # for exporters in self.telemetry_exporters:
        #     exporters.loaded_modules = self.loaded_agents

    def get_environment(self):
        """Get the current environment."""
        if os.path.exists("index.html"):
            # Development environment
            return Path(".")
        else:
            # Packaged environment
            return Path(__file__).resolve().parent

    def run_server(self):
        """Run the Schwarm server."""
        self._provider_manager.wait_for_frontend()

    def register_agent(self, agent: Agent):
        """Register an agent."""
        if any(a.name == agent.name for a in self._agents):
            logger.warning(f"Agent with name {agent.name} already exists.")
            return
        self._agents.append(agent)
        logger.info(f"Agent {agent.name} registered successfully.")

    @log_function_call(log_level="debug")
    def quickstart(
        self,
        agent: Agent,
        input: str = "",
        context_variables: dict[str, Any] | None = None,
        override_model: str = "",
    ) -> Response:
        """Run a single agent input."""
        return self.run(
            agent,
            messages=[Message(role="user", content=input)],
            context_variables=context_variables or {},
            override_model=override_model,
            max_turns=100,
            execute_tools=True,
            show_logs=True,
        )

    @log_function_call(log_level="debug")
    def run(
        self,
        agent: Agent,
        messages: list[Message],
        context_variables: dict[str, Any],
        override_model: str | None = None,
        max_turns: int = 10,
        execute_tools: bool = True,
        show_logs: bool = True,
    ) -> Response:
        """Run the agent through a conversation."""
        with self._telemetry_manager.global_tracer.start_as_current_span(f"SCHWARM_START") as parent_span:
            self._run_id = uuid.uuid4().hex
            self._telemetry_manager.run_id = self._run_id
            self._provider_manager.wait_for_frontend()
            setup_logging(is_logging_enabled=show_logs, log_level="trace")
            self._provider_context = ProviderContextModel()
            self._provider_context.breakpoint_counter = self._provider_manager.breakpoint_counter

            while True:
                with self._telemetry_manager.global_tracer.start_as_current_span(f"{agent.name}") as span:
                    parent_span.add_event(agent.name + " START")
                    self._telemetry_manager.send_any_object(agent, span)
                    span.set_attribute("agent_id", agent.name)
                    self._setup_context(agent, messages, context_variables, max_turns)
                    self._trigger_event(EventType.START_TURN)
                    logger.info(f"Processing turn {self._provider_context.current_turn}/{max_turns}")
                    self._process_turn(agent, context_variables, override_model, execute_tools)
                    self._provider_context.current_turn += 1
                    self._provider_manager.breakpoint_counter -= 1
                    if self._provider_manager.breakpoint_counter < 0:
                        self._provider_manager.breakpoint_counter = self._provider_context.breakpoint_counter
                    if not self._can_continue_conversation(agent):
                        span.end()
                        break
                    else:
                        messages = self._provider_context.message_history
                        agent = self._provider_context.current_agent
                        context_variables = self._provider_context.context_variables
                        max_turns = self._provider_context.max_turns
                        span.end()

            logger.info(f"Agent run completed after {self._provider_context.current_turn} turns")
            self._restore_logging(show_logs)

            final_response = Response(
                messages=self._provider_context.message_history[len(messages) :],
                agent=self._provider_context.current_agent,
                context_variables=self._provider_context.context_variables,
            )

            self._telemetry_manager.send_any_object(final_response, parent_span)
            parent_span.end()

        while True:
            time.sleep(0.5)

        return Response(
            messages=self._provider_context.message_history[len(messages) :],
            agent=self._provider_context.current_agent,
            context_variables=self._provider_context.context_variables,
        )

    def create_provider_configs(self, agent: Agent) -> dict[str, Any]:
        """Create provider configurations for an agent."""
        provider_configs = {}
        for config in agent.configs:
            if isinstance(config, BaseLLMProviderConfig):
                config.name = agent.model
                provider = self._provider_manager.create_provider(agent.name, config)
                provider_configs[provider.provider_name] = provider
                agent.provider_names.append(provider.provider_name)
            elif isinstance(config, BaseProviderConfig):
                provider = self._provider_manager.create_provider(agent.name, config)
                provider_configs[provider.provider_name] = provider
                agent.provider_names.append(provider.provider_name)
            if isinstance(config, TelemetryConfig):
                self._telemetry_manager.add_agent(agent.name, config)
        return provider_configs

    def _setup_context(
        self,
        agent: Agent,
        messages: list[Message],
        context_variables: dict[str, Any],
        max_turns: int,
    ):
        """Initialize the provider context."""
        if self._provider_context.current_turn == 0:
            self._provider_context = ProviderContextModel()
            self._provider_context.current_turn = 0
            self._provider_context.available_agents = [agent]
            self._provider_context.available_tools = agent.functions
            self.create_provider_configs(agent)
        else:
            if agent not in self._provider_context.available_agents:
                self._provider_context.available_agents.append(agent)
                self.create_provider_configs(agent)
            for function in agent.functions:
                if function not in self._provider_context.available_tools:
                    self._provider_context.available_tools.append(function)

        if isinstance(agent, UserAgent) and agent.default_handoff_agent:
            self._provider_context.default_handoff_agent = agent

        self._provider_context.max_turns = max_turns
        self._provider_context.current_agent = agent
        self._provider_context.context_variables = copy.deepcopy(context_variables)
        self._provider_context.message_history = copy.deepcopy(messages)
        self._provider_context.available_providers = self._provider_manager.get_all_provider_cfgs_as_dict()

    def _set_instructions(self, agent: Agent):
        """Set agent instructions in the context."""
        if callable(agent.instructions):
            self._provider_context.instruction_func = agent.instructions
            self._provider_context.instruction_str = agent.instructions(self._provider_context.context_variables)
        else:
            self._provider_context.instruction_func = None
            self._provider_context.instruction_str = agent.instructions

    def _can_continue_conversation(self, current_agent: Agent):
        """Check if the conversation can continue."""
        pm = self._provider_manager
        if isinstance(current_agent, UserAgent) and pm.last_user_input == "stop":
            return False
        if isinstance(current_agent, TerminatorAgent):
            return False
        if self._provider_context.max_turns == -1:
            return True
        return self._provider_context.current_turn < self._provider_context.max_turns

    def _process_turn(
        self, agent: Agent, context_variables: dict[str, Any], override_model: str | None, execute_tools: bool
    ):
        """Process a single turn in the conversation."""
        user_handoff = None
        if isinstance(agent, UserAgent):
            self._provider_manager.wait_for_frontend(True)
            completion = Message(role="user", content=self._provider_manager.last_user_input)
            user_handoff = agent.agent_to_pass_to
        else:
            completion = self._complete_agent_request(agent, context_variables, override_model)

        if self._provider_manager.chunk:
            self._provider_context.streamed_output = self._provider_manager.chunk
        else:
            self._provider_context.streamed_output = completion.content

        self._provider_context.current_message = completion
        self._provider_context.message_history.append(completion)
        self._provider_context.current_tools = completion.tool_calls
        self._trigger_event(EventType.POST_MESSAGE_COMPLETION)

        if not completion.tool_calls or not execute_tools:
            logger.info("No tools to execute or tool execution disabled")
            if self._provider_context.default_handoff_agent and not user_handoff:
                user_handoff = self._provider_context.default_handoff_agent
            if user_handoff:
                logger.info(f"Agent handoff: {agent.name} -> {user_handoff.name}")
                self._provider_context.current_agent = user_handoff
                self._provider_context.previous_agent = agent
                self._trigger_event(EventType.HANDOFF)
            return

        self._trigger_event(EventType.TOOL_EXECUTION)

        partial_response = ToolHandler().handle_tool_calls(
            current_agent=agent.name,
            tool_calls=completion.tool_calls,
            functions=agent.functions,
            context_variables=context_variables,
            provider_context=self._provider_context,
        )

        self._provider_context.message_history.extend(partial_response.messages)
        self._provider_context.context_variables.update(partial_response.context_variables)
        self._trigger_event(EventType.POST_TOOL_EXECUTION)

        if partial_response.agent and partial_response.agent != agent:
            logger.info(f"Agent handoff: {agent.name} -> {partial_response.agent.name}")
            self._provider_context.current_agent = partial_response.agent
            self._provider_context.previous_agent = agent
            self._trigger_event(EventType.HANDOFF)

    def _restore_logging(self, show_logs: bool):
        """Restore logging settings if modified."""
        if not show_logs:
            self._default_handler = logger.add(sys.stderr, level="DEBUG")

    @log_function_call(log_level="DEBUG")
    def _complete_agent_request(self, agent: Agent, context_variables: dict[str, Any], override_model: str) -> Message:
        """Complete an agent request."""
        context_variables = defaultdict(str, context_variables)  # type: ignore

        self._set_instructions(agent)
        self._trigger_event(EventType.INSTRUCT)

        system_msg = Message(role="system", content=self._provider_context.instruction_str)
        messages = [system_msg, *self._provider_context.message_history]

        tools = [function_to_json(f) for f in agent.functions]
        self._filter_context_vars_from_tools(tools)
        self._trigger_event(EventType.MESSAGE_COMPLETION)
        provider = self._provider_manager.get_first_llm_provider(agent.name)
        if isinstance(provider, LLMProvider):
            result = provider.complete(
                messages,
                override_model=override_model,
                tools=tools,
                tool_choice=str(agent.tool_choice),
                parallel_tool_calls=agent.parallel_tool_calls,
                agent_name=agent.name,
            )
            if result and result.info:
                self._provider_context.current_agent.token_spent = result.info.token_counter
                self._provider_context.current_agent.total_cost = result.info.completion_cost

        return result

    def _filter_context_vars_from_tools(self, tools: list[dict]):
        """Remove context variables from tool parameters."""
        for tool in tools:
            params = tool["function"]["parameters"]
            params["properties"].pop(APP_SETTINGS.CONTEXT_VARS_KEY, None)
            if APP_SETTINGS.CONTEXT_VARS_KEY in params["required"]:
                params["required"].remove(APP_SETTINGS.CONTEXT_VARS_KEY)

    def pause(self, event_type: EventType = EventType.INSTRUCT):
        """Pause the conversation."""
        if self._provider_manager.breakpoint[event_type]:
            self._provider_manager.wait_for_frontend()
            return

        if self._provider_manager._global_break:
            self._provider_manager.wait_for_frontend()

    def _trigger_event(self, event_type: EventType):
        """Trigger a specific event."""
        logger.debug(f"Event triggered: {event_type}")

        # Check if the event should be logged or break the execution
        log_point = False
        if self.telemetry_exporters:
            for exporter in self.telemetry_exporters:
                if event_type in exporter.config.break_on_events:
                    self._provider_manager._global_break = True
                if event_type in exporter.config.log_on_events:
                    log_point = True

        # Send the event to the telemetry manager
        if log_point and self._telemetry_manager and self._run_id:
            event = create_event(self._provider_context, event_type)
            if event:
                self._telemetry_manager.send_trace(event)

        # Send the event to the provider manager
        if self._provider_context:
            event = create_full_event(self._provider_context, event_type)
            if self._provider_context and event:
                event.context = self._provider_context
                self._provider_manager.trigger_event(event, self._provider_context)

        self.pause(event_type)
