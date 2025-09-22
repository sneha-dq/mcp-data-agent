import time
from typing import Iterator
from core.primitives import ModelContext
from core.server import MCPServer

class ChatAgent:
    def __init__(self, model: str, server: MCPServer, call_model_func):
        self.model = model
        self.server = server
        self.call_model_func = call_model_func

    def handle(self, user_input: str) -> Iterator[str]:
        ctx = ModelContext(id=f"chat-{int(time.time())}")
        ctx.add_history("user", user_input)
        return self.call_model_func(self.model, user_input, ctx)