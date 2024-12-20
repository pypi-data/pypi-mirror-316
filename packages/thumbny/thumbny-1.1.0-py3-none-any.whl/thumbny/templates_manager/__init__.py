from __future__ import annotations

from typing import Dict
from typing import Any
from typing import List

import os
import sys

from thumbny.models import TemplateModel
from thumbny.templates_manager.file_handler import FileHandler
from thumbny.templates_manager.validator import Validator


class TemplateManager:
    def __new__(cls) -> TemplateManager:
        if not hasattr(cls, "_instance"):
            cls._instance = super(TemplateManager, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.templates_path = os.path.join(sys.path[0],
                                           "thumny-templates",
                                           "templates")

        self.file_handler = FileHandler(self, self.templates_path)
        self.validtor = Validator(self, self.templates_path)

    def create(self, model: TemplateModel) -> None:
        self.validtor.validate_tempalate_key(model.key)
        self.file_handler.create_template_dir(self.templates_path)
        template_Path = self.file_handler.create_template_structure(model.key)
        self.file_handler.copy_fonts(model, template_Path)
        self.file_handler.save_config(model, template_Path)

    def delete(self, name: str) -> None:
        self.file_handler.delete_template(name)

    def get_all_templates(self) -> List[str]:
        return self.file_handler.get_all_templates()

    def get_template_info(self, name: str) -> Dict[str, Any]:
        return self.file_handler.get_template_info(name)
