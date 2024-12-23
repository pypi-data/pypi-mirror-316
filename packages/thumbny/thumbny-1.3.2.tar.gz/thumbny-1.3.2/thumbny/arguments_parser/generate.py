from typing import Dict
from typing import Any
from typing import Optional

from thumbny.base import RunnerBase
from thumbny.commands import GenerateCommand
from thumbny.models import FillerModel


class GenerateRunner(RunnerBase):
    def __init__(self, arguments: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(arguments)

    def build(self, json_dict: dict) -> FillerModel:
        return FillerModel.make(json_dict)

    def execute(self) -> None:
        command = GenerateCommand(self.model,
                                  should_present=self.arguments.get("show"))
        command.execute()
