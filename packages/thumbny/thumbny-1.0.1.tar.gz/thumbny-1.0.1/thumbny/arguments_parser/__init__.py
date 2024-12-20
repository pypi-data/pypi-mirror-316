import argparse
from argparse import ArgumentParser as AP
from argparse import _SubParsersAction
from argparse import Namespace

from thumbny.base import runner
from thumbny.arguments_parser.create import CreateRunner
from thumbny.arguments_parser.delete import DeleteRunner
from thumbny.arguments_parser.generate import GenerateRunner
from thumbny.arguments_parser.info import InfoRunner
from thumbny.arguments_parser.templates import TemplatesRunner


COMMANDS = {"create": CreateRunner,
            "delete": DeleteRunner,
            "generate": GenerateRunner,
            "info": InfoRunner,
            "templates": TemplatesRunner,
            }


class Parser:
    def _register_create(self, subparser: _SubParsersAction) -> None:
        parser: AP = subparser.add_parser("create",
                                          help="Create a new template")

        parser.add_argument("-d", "--data",
                            help="json data")

    def _register_delete(self, subparser: _SubParsersAction) -> None:
        parser: AP = subparser.add_parser("delete",
                                          help="Delete a template")

        parser.add_argument("-d", "--data",
                            help="json data")

    def _register_generate(self, subparser: _SubParsersAction) -> None:
        parser: AP = subparser.add_parser("generate",
                                          help="Generate a thumbnail")

        parser.add_argument("-d", "--data",
                            help="json data")

    def _register_info(self, subparser: _SubParsersAction) -> None:
        parser: AP = subparser.add_parser("info", help="Info of a template")

        parser.add_argument("-d", "--data",
                            help="json data")

    def _register_templates(self, subparser: _SubParsersAction) -> None:
        subparser.add_parser("templates", help="List all templates")

    def _execute(self, args: Namespace) -> None:
        command_ref = COMMANDS.get(args.command)
        arguments = dict(args._get_kwargs())
        command: runner = command_ref(json_string=arguments.get("data"))
        command.execute()

    def parse(self) -> None:
        parser = argparse.ArgumentParser()
        subparser = parser.add_subparsers(dest="command", required=True)
        self._register_create(subparser)
        self._register_delete(subparser)
        self._register_generate(subparser)
        self._register_info(subparser)
        self._register_templates(subparser)
        args = parser.parse_args()
        self._execute(args)
