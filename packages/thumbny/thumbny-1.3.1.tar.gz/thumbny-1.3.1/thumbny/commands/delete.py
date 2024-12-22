from thumbny.base import CommandBase
from thumbny.models import TemplateNameModel


class DeleteCommand(CommandBase):
    def __init__(self, model: TemplateNameModel) -> None:
        super().__init__()
        self.model = model

    def execute(self) -> None:
        self.tm.delete(self.model.name)
        print(f"{self.model.name} template has been deleted successfully")
