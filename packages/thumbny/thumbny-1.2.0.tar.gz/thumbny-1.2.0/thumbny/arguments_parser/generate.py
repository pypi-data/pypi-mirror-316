from typing import Optional

from thumbny.base import RunnerBase
from thumbny.commands import GenerateCommand
from thumbny.models import FillerModel


class GenerateRunner(RunnerBase):
    def __init__(self, json_string: Optional[str] = None) -> None:
        super().__init__(json_string)

    def build(self, json_dict: dict) -> FillerModel:
        return FillerModel.make(json_dict)

    def execute(self) -> None:
        command = GenerateCommand(self.model)
        command.execute()
