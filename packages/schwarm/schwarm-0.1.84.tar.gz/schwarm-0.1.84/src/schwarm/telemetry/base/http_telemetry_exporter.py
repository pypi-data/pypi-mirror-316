"""Base class for custom OpenTelemetry exporters."""

import asyncio
import mimetypes
import socket
from abc import ABC, abstractmethod
from threading import Thread

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger
from opentelemetry.sdk.trace.export import SpanExportResult
from socketio import ASGIApp, AsyncServer

from schwarm.configs.telemetry_config import TelemetryConfig
from schwarm.manager.stream_manager import StreamManager
from schwarm.provider.provider_manager import ProviderManager
from schwarm.telemetry.base.telemetry_exporter import TelemetryExporter
from schwarm.telemetry.socketio_manager import SocketIOManager
from schwarm.utils.settings import get_environment


class HttpTelemetryExporter(TelemetryExporter, ABC):
    """Base class for custom OpenTelemetry exporters."""

    def __init__(self, config: TelemetryConfig, api_host="127.0.0.1", api_port=8123):
        """Initialize the base exporter."""
        super().__init__(config)
        self.api_host = api_host
        self.api_port = api_port
        self.app = FastAPI()
        self.loaded_modules = {}

        # Initialize Socket.IO
        self.sio = AsyncServer(async_mode='asgi', cors_allowed_origins="*")
        self.socket_app = ASGIApp(self.sio)

        # Set up the Socket.IO server in the manager
        SocketIOManager().set_server(self.sio)

        mimetypes.add_type("application/javascript", ".js")
        mimetypes.add_type("application/javascript", ".mjs")

        # Base directory for static files
        self.base_dir = get_environment().parent.parent.joinpath("schwarm")
        index_file_path = self.base_dir.joinpath("index.html")
        assets_dir = self.base_dir.joinpath("assets")

        # Configure CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Allows all origins
            allow_credentials=True,
            allow_methods=["*"],  # Allows all methods
            allow_headers=["*"],  # Allows all headers
        )

        # Mount static assets and Socket.IO
        if index_file_path.exists() and assets_dir.exists():
            logger.info(f"Serving static files from: {self.base_dir}")
            self.app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
            self.app.mount("/socket.io", self.socket_app)
        else:
            raise FileNotFoundError(f"Static files not found in {self.base_dir}")

        self._configure_api()
        self._configure_socketio()
        self._start_api()

    def _export(self, spans):
        """Forward spans to the backend."""
        try:
            result = self.export(spans)
            if result is None:
                return SpanExportResult.SUCCESS
            return result
        except Exception:
            return SpanExportResult.FAILURE
        finally:
            self.shutdown()

    def find_free_port(self, start_port=8123, max_port=9000):
        """Find a free port starting from `start_port`."""
        for port in range(start_port, max_port + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    # Try binding to the port
                    s.bind(("127.0.0.1", port))
                    return port  # Port is free
                except OSError:
                    continue  # Port is in use, try next
        raise RuntimeError("No free port found in the specified range.")

    @abstractmethod
    def query_spans(self):
        """Retrieve all spans. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement the query_spans method")

    @abstractmethod
    def query_span_by_id(self, span_id):
        """Retrieve a span by ID. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement the query_span_by_id method")

    @abstractmethod
    def query_spans_after_id(self, after_id):
        """Retrieve all spans created after the given span ID. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement the query_spans_after_id method")

    def _configure_socketio(self):
        """Configure Socket.IO event handlers."""
        @self.sio.event
        async def connect(sid, environ):
            """Handle Socket.IO connection."""
            logger.debug(f"Socket.IO client connected: {sid}")
            SocketIOManager().active_connections.add(sid)

        @self.sio.event
        async def disconnect(sid):
            """Handle Socket.IO disconnection."""
            logger.debug(f"Socket.IO client disconnected: {sid}")
            SocketIOManager().active_connections.remove(sid)

        @self.sio.event
        async def stream(sid, data):
            """Handle stream events."""
            try:
                await StreamManager().handle_stream(sid, data)
            except Exception as e:
                logger.error(f"Error handling stream: {e}")
                await self.sio.emit('error', {'message': str(e)}, room=sid)

    def _configure_api(self):
        """Set up API endpoints for querying spans."""

        @self.app.get("/", include_in_schema=False)
        def serve_index():
            """Serve the index.html file."""
            return FileResponse(str(self.base_dir.joinpath("index.html")))

        @self.app.post("/break")
        def set_break():
            """Toggle the global break state."""
            pm = ProviderManager._instance
            if pm:
                pm._global_break = not pm._global_break
                return pm._global_break

        @self.app.post("/breakpoint/turns")
        def set_breakpoint_number(turn_amount: int):
            """Toggle the global break state."""
            pm = ProviderManager._instance
            if pm:
                pm.breakpoint_counter = turn_amount - 1
                return pm.breakpoint_counter

        @self.app.get("/breakpoint/turns")
        def get_breakpoint_number():
            """Toggle the global break state."""
            pm = ProviderManager._instance
            if pm:
                return pm.breakpoint_counter

        @self.app.post("/breakpoint")
        def toggle_breakpoint(event_type: str):
            """Toggle the global break state."""
            pm = ProviderManager._instance
            if pm:
                pm.toggle_breakpoint(event_type)
                return pm.breakpoint

        @self.app.get("/breakpoint")
        def show_breakpoints():
            """Toggle the global break state."""
            pm = ProviderManager._instance
            if pm:
                return pm.breakpoint

        @self.app.post("/chat")
        def post_chat(user_input: str):
            """Toggle the global break state."""
            pm = ProviderManager._instance
            if pm:
                pm._global_break = not pm._global_break
                pm.last_user_input = user_input
                return user_input

        @self.app.get("/chat")
        def is_waiting_for_user_input():
            """Toggle the global break state."""
            pm = ProviderManager._instance
            if pm:
                return pm._global_break & pm.wait_for_user_input

        @self.app.get("/break")
        def get_break():
            """Get the current break state."""
            pm = ProviderManager._instance
            if pm:
                return pm._global_break

        @self.app.get("/spans")
        def get_spans(after_id: str | None = None):
            """Retrieve spans, optionally filtered by after_id."""
            if after_id:
                return self.query_spans_after_id(after_id)
            return self.query_spans()

        @self.app.get("/spans/{span_id}")
        def get_span_by_id(span_id: str):
            """Retrieve a span by its ID."""
            return self.query_span_by_id(span_id)

        @self.app.get("/load")
        def get_loaded_modules():
            """Retrieve a span by its ID."""
            result = ""
            for obj in self.loaded_modules:
                result += obj[1].name
            return f"{result}"

    def _start_api(self):
        """Start the FastAPI server in a separate thread."""
        def run():
            port = self.find_free_port(self.api_port)
            config = uvicorn.Config(
                self.app,
                host=self.api_host,
                port=port,
                log_level="error",
            )
            server = uvicorn.Server(config)
            server.run()

        thread = Thread(target=run, daemon=True)
        thread.start()
