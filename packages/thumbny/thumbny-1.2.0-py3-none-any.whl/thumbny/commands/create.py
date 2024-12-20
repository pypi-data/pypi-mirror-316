
from thumbny.base import CommandBase
from thumbny.models import TemplateModel


class CreateCommand(CommandBase):
    def __init__(self, model: TemplateModel):
        super().__init__()
        self.model = model

    def execute(self):
        self.tm.create(self.model)
        print(f"{self.model.key} template has been created successfully")
