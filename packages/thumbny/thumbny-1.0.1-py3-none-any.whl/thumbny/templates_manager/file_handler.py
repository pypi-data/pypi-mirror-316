from typing import TYPE_CHECKING
from typing import List

import os
import re
import json
import shutil
from dataclasses import asdict

from thumbny.models import TemplateModel
from thumbny.exceptions import TemplateNotExist

if TYPE_CHECKING:
    from thumbny.templates_manager import TemplateManager


FILE_NAME_REGEX = r'[^\\|^/]+$'


class FileHandler:
    def __init__(self,
                 template_manager: "TemplateManager",
                 templates_path: str) -> None:
        self.template_manager = template_manager
        self.templates_path = templates_path

    def create_template_dir(self, templates_path: str) -> None:
        if not os.path.exists(templates_path):
            os.makedirs(templates_path)

    def create_template_structure(self, key: str) -> str:
        template_path = os.path.join(self.templates_path, key)
        os.mkdir(template_path)
        os.mkdir(os.path.join(template_path, "assets"))
        os.mkdir(os.path.join(template_path, "assets", "fonts"))
        return template_path

    def copy_fonts(self, model: TemplateModel, template_path: str) -> None:
        for label in model.labels:
            if label.font_family:
                font_name = re.search(FILE_NAME_REGEX,
                                      label.font_family).group(0)

                font_path = os.path.join(template_path,
                                         "assets",
                                         "fonts",
                                         font_name)

                shutil.copyfile(label.font_family, font_path)
                label.font_family = font_path

    def save_config(self, config: TemplateModel, template_path: str) -> None:
        config_path = os.path.join(template_path, "config.json")
        with open(config_path, "w") as f:
            json.dump(asdict(config), f, indent=4)

    def delete_template(self, name: str) -> None:
        try:
            path = os.path.join(self.templates_path, name)
            shutil.rmtree(path)
        except FileNotFoundError:
            raise TemplateNotExist(f"{name} template does not exist")

    def get_all_templates(self) -> List[str]:
        if not os.path.exists(self.templates_path):
            return []

        return [element for element in os.listdir(self.templates_path)
                if os.path.isdir(os.path.join(self.templates_path, element))]

    def get_template_info(self, name: str) -> dict:
        path = os.path.join(self.templates_path, name, "config.json")
        if not os.path.isfile(path):
            raise TemplateNotExist(f"{name} template does not exist")
        with open(path) as f:
            return json.load(f)
