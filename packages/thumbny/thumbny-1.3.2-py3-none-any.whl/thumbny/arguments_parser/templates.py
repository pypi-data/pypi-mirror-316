from typing import Dict
from typing import Any
from typing import Optional

from thumbny.base import RunnerBase
from thumbny.commands import TemplatesCommand


class TemplatesRunner(RunnerBase):
    def __init__(self, arguments: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(arguments)

    def execute(self) -> None:
        command = TemplatesCommand()
        return command.execute()
