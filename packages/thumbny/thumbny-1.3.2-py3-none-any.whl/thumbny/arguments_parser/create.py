from typing import Dict
from typing import Any
from typing import Optional

from thumbny.base import RunnerBase
from thumbny.commands import CreateCommand
from thumbny.models import TemplateModel


class CreateRunner(RunnerBase):
    def __init__(self, arguments: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(arguments)

    def build(self, json_dict: Dict[str, Any]) -> TemplateModel:
        return TemplateModel.make(json_dict)

    def execute(self) -> None:
        command = CreateCommand(self.model)
        command.execute()
