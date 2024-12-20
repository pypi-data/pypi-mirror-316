from __future__ import annotations

from typing import List
from typing import Dict
from typing import Any
from dataclasses import dataclass

from thumbny.models.shared import TagModel
from thumbny.models.validation import check_required_fields


@dataclass
class FillerModel:
    name: str
    template_key: str
    labels: List[TagModel]

    def __post_init__(self):
        check_required_fields(self)

    @classmethod
    def make(cls, data: Dict[str, Any]) -> FillerModel:
        labels = []
        for label in data.get("labels", []):
            labels.append(TagModel.make(label))

        return cls(name=data.get("name"),
                   template_key=data.get("template_key"),
                   labels=labels)
