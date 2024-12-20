from __future__ import annotations

from typing import Dict
from typing import List
from typing import Optional
from typing import Any
from dataclasses import dataclass

from thumbny.models.shared import TagModel
from thumbny.models.validation import check_required_fields
from thumbny.models.validation import check_spaces
from thumbny.models.validation import check_hex_color


@dataclass
class LabelModel:
    key: str
    content: str
    position: TagModel
    alignment: Optional[str]
    font_color: str
    font_size: int
    font_family: Optional[str]

    def __post_init__(self):
        check_required_fields(self)

    @classmethod
    def make(cls, data: Dict[str, Any]) -> LabelModel:
        position = TagModel.make(data.get("position"))
        return LabelModel(key=data.get("key"),
                          content=data.get("content"),
                          position=position,
                          alignment=data.get("alignment"),
                          font_color=data.get("font_color"),
                          font_size=data.get("font_size"),
                          font_family=data.get("font_family"))


@dataclass
class TemplateModel:
    key: str
    name: str
    width: int
    height: int
    background_color: str
    labels: List[LabelModel]

    def __post_init__(self):
        check_required_fields(self)
        check_spaces("key", self.key)
        check_hex_color("background_color", self.background_color)

    @classmethod
    def make(cls, data: Dict[str, Any]) -> TemplateModel:
        labels = []
        for label in data.get("labels", []):
            label = LabelModel.make(label)
            labels.append(label)

        return cls(key=data.get("key"),
                   name=data.get("name"),
                   width=data.get("width"),
                   height=data.get("height"),
                   background_color=data.get("background_color"),
                   labels=labels)
