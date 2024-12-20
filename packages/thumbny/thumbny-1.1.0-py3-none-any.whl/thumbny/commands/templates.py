from thumbny.templates_manager import TemplateManager
from thumbny.base import CommandBase


class TemplatesCommand(CommandBase):
    def __init__(self) -> None:
        self.template_manager = TemplateManager()

    def execute(self) -> None:
        templates = self.template_manager.get_all_templates()
        if templates:
            print("List of templates:")
            for x, y in enumerate(templates):
                print(f"{x+1}. {y}")
        else:
            print("No templates have been found")
