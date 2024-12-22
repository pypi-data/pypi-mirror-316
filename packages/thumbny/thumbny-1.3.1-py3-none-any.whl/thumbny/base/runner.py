from typing import Dict
from typing import Any
from typing import Optional

import json
from dataclasses import dataclass


class RunnerBase:
    def __init__(self, json_string: Optional[str] = None):
        self.model = None

        if json_string:
            json_dict = json.loads(json_string)
            self.model = self.build(json_dict)

    def build(self, json_dict: Dict[str, Any]) -> dataclass:
        return NotImplementedError()

    def execute(self) -> None:
        raise NotImplementedError()
