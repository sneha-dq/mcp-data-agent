from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
import time

@dataclass
class ModelContext:
    id: str
    created_at: float = field(default_factory=lambda: time.time())
    history: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    docs: List[Dict[str, Any]] = field(default_factory=list)

    def add_history(self, role: str, text: str):
        self.history.append({"role": role, "text": text})

    def to_mcp_payload(self):
        return asdict(self)