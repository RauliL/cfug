import os

from jinja2 import Template
from pathlib import Path
from pathvalidate import sanitize_filename
from typing import Any, Dict, Optional


class ProjectTemplate:
    @classmethod
    def find(cls, name: str) -> Optional["ProjectTemplate"]:
        directory = os.path.realpath(
            os.path.join(os.path.realpath(__file__), "..", sanitize_filename(name))
        )

        if not os.path.isdir(directory):
            return None

        return cls(directory=Path(directory))

    def __init__(self, directory: Path):
        self.directory = directory

    def install(self, target_directory: Path, context: Dict[str, Any]):
        self._install_traverse(
            source_directory=self.directory,
            target_directory=target_directory,
            context=context,
        )

    def _install_traverse(
        self, source_directory: Path, target_directory: Path, context: Dict[str, Any]
    ):
        for filename in os.listdir(source_directory):
            if filename.startswith("."):
                continue

            full_source_filename = source_directory.joinpath(filename)
            if os.path.isdir(full_source_filename):
                full_target_filename = target_directory.joinpath(filename)
                os.mkdir(full_target_filename)
                self._install_traverse(
                    source_directory=full_source_filename,
                    target_directory=full_target_filename,
                    context=context,
                )
            else:
                self._install_file(
                    source_directory=source_directory,
                    target_directory=target_directory,
                    filename=filename,
                    context=context,
                )

    def _install_file(
        self,
        source_directory: Path,
        target_directory: Path,
        filename: str,
        context: Dict[str, Any],
    ):
        source_filename = source_directory.joinpath(filename)
        target_filename = target_directory.joinpath(
            f".{filename[1:]}" if filename.startswith("_") else filename,
        )

        with open(source_filename, "r") as f:
            template = Template(f.read(), autoescape=False)

        with open(target_filename, "w") as f:
            f.write(template.render(context))
