from __future__ import annotations

from typing import Dict
from typing import Any

from dataclasses import dataclass


@dataclass
class TemplateNameModel:
    name: str

    @classmethod
    def make(cls, data: Dict[str, Any]) -> TemplateNameModel:
        return cls(name=data.get("name"))
