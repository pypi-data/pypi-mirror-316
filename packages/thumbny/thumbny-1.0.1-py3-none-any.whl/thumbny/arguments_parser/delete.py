from typing import Dict
from typing import Any
from typing import Optional

from thumbny.base import RunnerBase
from thumbny.commands import DeleteCommand
from thumbny.models import TemplateNameModel


class DeleteRunner(RunnerBase):
    def __init__(self, json_string: Optional[str] = None) -> None:
        super().__init__(json_string)

    def build(self, json_dict: Dict[str, Any]) -> TemplateNameModel:
        return TemplateNameModel.make(json_dict)

    def execute(self) -> None:
        command = DeleteCommand(self.model)
        return command.execute()
