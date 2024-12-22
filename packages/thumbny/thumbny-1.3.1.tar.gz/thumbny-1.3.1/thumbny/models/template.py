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
class PaddingModel:
    top: int
    bottom: int
    left: int
    right: int

    def __post_init__(self) -> None:
        check_required_fields(self)

    @classmethod
    def make(cls, data: Dict[str, Any]) -> PaddingModel:
        return cls(top=data.get("top"),
                   bottom=data.get("bottom"),
                   left=data.get("left"),
                   right=data.get("right"))


@dataclass
class LabelModel:
    key: str
    content: str
    position: TagModel
    padding: Optional[PaddingModel]
    font_color: str
    font_size: int
    font_family: Optional[str]
    alignment: Optional[str]

    def __post_init__(self) -> None:
        check_required_fields(self)

    @classmethod
    def make(cls, data: Dict[str, Any]) -> LabelModel:
        position = TagModel.make(data.get("position"))

        padding = None
        if data.get("padding"):
            padding = PaddingModel.make(data.get("padding"))

        return cls(key=data.get("key"),
                   content=data.get("content"),
                   position=position,
                   padding=padding,
                   font_color=data.get("font_color"),
                   font_size=data.get("font_size"),
                   font_family=data.get("font_family"),
                   alignment=data.get("alignment"),)


@dataclass
class TemplateModel:
    key: str
    name: str
    width: int
    height: int
    background_color: str
    background_image: Optional[str]
    labels: List[LabelModel]

    def __post_init__(self) -> None:
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
                   background_image=data.get("background_image"),
                   labels=labels)
