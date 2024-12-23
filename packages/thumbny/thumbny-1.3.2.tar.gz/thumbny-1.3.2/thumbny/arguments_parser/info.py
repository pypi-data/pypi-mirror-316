from typing import Dict
from typing import Any
from typing import Optional

from thumbny.base import RunnerBase
from thumbny.commands import InfoCommand
from thumbny.models import TemplateNameModel


class InfoRunner(RunnerBase):
    def __init__(self, arguments: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(arguments)

    def build(self, json_dict: Dict[str, Any]) -> TemplateNameModel:
        return TemplateNameModel.make(json_dict)

    def execute(self) -> None:
        command = InfoCommand(self.model)
        return command.execute()
