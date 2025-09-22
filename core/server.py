from typing import Any, Dict

class MCPServer:
    """Minimal MCP Server: holds resources, tools, and dispatch logic."""
    def __init__(self):
        self.resources: Dict[str, Any] = {}
        self.tools: Dict[str, Any] = {}

    def register_resource(self, name: str, data: Any):
        self.resources[name] = data

    def register_tool(self, name: str, func):
        self.tools[name] = func

    def run_tool(self, name: str, *args, **kwargs):
        if name not in self.tools:
            raise ValueError(f"Tool {name} not found")
        return self.tools[name](*args, **kwargs)