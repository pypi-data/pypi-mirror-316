import asyncio
import inspect
from typing import Callable

from .handlers import HTTPHandler, RawHandler, WebSocketHandler
from .router import Router
from .server import Server
from .websocket import WebSocketConnection


def is_async_func(func):
    return inspect.iscoroutinefunction(func)


class MiniAPI:
    def __init__(self):
        self.router = Router()
        self.middleware = []
        self.debug = False
        self.event_handlers = {"startup": [], "shutdown": []}

    def get(self, path: str):
        return self.router.get(path)

    def post(self, path: str):
        return self.router.post(path)

    def put(self, path: str):
        return self.router.put(path)

    def delete(self, path: str):
        return self.router.delete(path)

    def websocket(self, path: str):
        return self.router.websocket(path)

    def add_middleware(self, middleware, **kwargs):
        """添加中间件"""
        self.middleware.append((middleware, kwargs))

    def on_event(self, event: str):
        if event in self.event_handlers:

            def decorator(handler):
                self.event_handlers[event].append(handler)

            return decorator
        else:
            raise ValueError(f"Unknown event type: {event}")

    async def _handle_websocket(self, websocket, path):
        """Handle WebSocket connections"""
        if path in self.router.websocket_handlers:
            handler = self.router.websocket_handlers[path]
            conn = WebSocketConnection(websocket)
            if len(inspect.signature(handler).parameters) > 0:
                await handler(conn)
            else:
                await handler()

    async def __call__(self, scope: dict, receive: Callable, send: Callable) -> None:
        """ASGI application interface"""
        if scope["type"] == "http":
            await HTTPHandler.handle(self, scope, receive, send)
        elif scope["type"] == "websocket":
            await WebSocketHandler.handle(self, scope, receive, send)
        elif scope["type"] == "lifespan":
            while True:
                message = await receive()
                if message["type"] == "lifespan.startup":
                    for handler in self.event_handlers["startup"]:
                        if is_async_func(handler):
                            await handler()
                        else:
                            handler()
                    await send({"type": "lifespan.startup.complete"})
                elif message["type"] == "lifespan.shutdown":
                    for handler in self.event_handlers["shutdown"]:
                        if is_async_func(handler):
                            await handler()
                        else:
                            handler()
                    await send({"type": "lifespan.shutdown.complete"})
                    break
        else:
            raise ValueError(f"Unknown scope type: {scope['type']}")

    async def handle_request(self, reader, writer):
        await RawHandler.handle(self, reader, writer)

    def run(self, host: str = "127.0.0.1", port: int = 8000):
        asyncio.get_event_loop().run_until_complete(Server.run_server(self, host, port))
