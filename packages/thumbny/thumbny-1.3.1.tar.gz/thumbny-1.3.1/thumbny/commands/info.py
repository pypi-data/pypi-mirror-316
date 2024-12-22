from typing import Dict
from typing import Any

from thumbny.base import CommandBase
from thumbny.models import TemplateNameModel


class InfoCommand(CommandBase):
    def __init__(self, model: TemplateNameModel) -> None:
        super().__init__()
        self.model = model

    def _print_info(self,
                    details: Dict[str, Any],
                    post_indent: int = 0,
                    indent: int = 20) -> None:
        for x, y in details.items():
            if isinstance(y, list):
                for record in details[x]:
                    self._print_info(record, post_indent+5, indent)
                return None
            elif isinstance(y, dict):
                self._print_info(y, post_indent+5, indent)
                return None
            else:
                print(f"{'':<{post_indent}} {x:<{indent}} {y}")

    def execute(self) -> None:
        details = self.tm.get_template_info(self.model.name)
        print("="*40)
        print(f"{'Key':<20} {'Value'}")
        print("="*40)
        self._print_info(details)
