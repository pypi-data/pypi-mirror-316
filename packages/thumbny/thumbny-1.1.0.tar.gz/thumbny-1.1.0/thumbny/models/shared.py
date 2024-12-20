from __future__ import annotations

from typing import Dict
from typing import Any

from dataclasses import dataclass

from thumbny.models.validation import check_required_fields


@dataclass
class TagModel:
    key: str
    value: str

    def __post_init__(self):
        check_required_fields(self)

    @classmethod
    def make(cls, data: Dict[str, Any]) -> TagModel:
        return cls(key=data.get("key"),
                   value=data.get("value"))
