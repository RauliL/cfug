import os
import pygit2  # type: ignore
import subprocess
import sys

from caseconvertor import camelcase  # type: ignore
from pathlib import Path
from typing import Any, Optional

from .exceptions import ProjectNotConfiguredError, ProjectNotFoundError
from .template import ProjectTemplate


class Project:
    @classmethod
    def find(cls) -> "Project":
        path = Path.cwd()

        while str(path) != path.root:
            if path.joinpath(".cfug").exists():
                return cls(root_directory=path)
            path = path.parent

        raise ProjectNotFoundError()

    def __init__(self, root_directory: Path):
        self.root_directory = root_directory

    @property
    def name(self) -> str:
        name = camelcase(os.path.basename(self.root_directory))
        return f"{name[0].upper()}{name[1:]}"

    @property
    def build_directory(self) -> Path:
        return self.root_directory.joinpath("build")

    def create(
        self,
        template: ProjectTemplate,
        version: Optional[str] = None,
        description: Optional[str] = None,
        homepage_url: Optional[str] = None,
        license: Optional[Any] = None,
        author: Optional[str] = "",
        email: Optional[str] = "",
    ):
        # Create the project directory.
        self.root_directory.mkdir()

        # Create empty ".cfug" marker file.
        with self.root_directory.joinpath(".cfug").open("w"):
            pass

        # Initialize git repository.
        pygit2.init_repository(self.root_directory)

        # Render license, if one was given.
        if license:
            with self.root_directory.joinpath("LICENSE").open("w") as f:
                f.write(license.render(name=author, email=email))

        # Install the template.
        template.install(
            self.root_directory,
            {
                "project": self,
                "version": version,
                "description": description,
                "homepage_url": homepage_url,
            },
        )

    def configure(self, *args):
        build_directory = self.build_directory
        if not build_directory.is_dir():
            build_directory.mkdir()

        subprocess.run(
            args=["cmake", "..", *args],
            stdout=sys.stdout,
            stderr=sys.stderr,
            cwd=build_directory,
        )

    def run_cmake(self, *args):
        build_directory = self.build_directory
        if not build_directory.joinpath("Makefile").exists():
            raise ProjectNotConfiguredError()

        subprocess.run(
            args=["cmake", *args],
            stdout=sys.stdout,
            stderr=sys.stderr,
            cwd=build_directory,
        )
