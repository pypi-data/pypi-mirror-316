from thumbny.templates_manager import TemplateManager


class CommandBase:
    def __init__(self) -> None:
        self.tm = TemplateManager()

    def execute() -> None:
        raise NotImplementedError()
