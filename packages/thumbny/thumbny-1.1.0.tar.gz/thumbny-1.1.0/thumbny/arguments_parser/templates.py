from typing import Optional

from thumbny.base import RunnerBase
from thumbny.commands import TemplatesCommand


class TemplatesRunner(RunnerBase):
    def __init__(self, json_string: Optional[str] = None) -> None:
        super().__init__(json_string)

    def execute(self) -> None:
        command = TemplatesCommand()
        return command.execute()
