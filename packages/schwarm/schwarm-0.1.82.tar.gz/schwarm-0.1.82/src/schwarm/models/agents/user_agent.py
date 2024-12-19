"""User agent for interacting with the system."""

from schwarm.models.agent import Agent, Result
from schwarm.provider.user_interaction_provider import UserInteractionConfig


class UserAgent(Agent):
    """An agent which does nothing except routing user messages into the system."""

    def pass_to(self) -> Result:
        return Result(agent=self.agent_to_pass_to)

    def __init__(self, agent_to_pass_to: Agent):
        super().__init__()
        self.name = "UserAgent"
        self.model = "gpt-4"
        self.agent_to_pass_to = agent_to_pass_to
        self.description = "User agent for interacting with the system."
        self.instructions = "You are a user agent."
        self.functions = [self.pass_to]
        self.tool_choice = "none"
        self.token_spent = 0
        self.total_cost = 0.0
        self.parallel_tool_calls = False
        self.configs = [UserInteractionConfig()]
        self.provider_names = []
