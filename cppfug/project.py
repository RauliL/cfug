import os
import pygit2

from caseconvertor import camelcase
from typing import Optional

from .template import ProjectTemplate


class Project:
    def __init__(
        self,
        root_directory: str,
        version: Optional[str] = None,
        description: Optional[str] = None,
        homepage_url: Optional[str] = None,
    ):
        self.root_directory = root_directory
        self.version = version
        self.description = description
        self.homepage_url = homepage_url

    @property
    def name(self) -> str:
        name = camelcase(os.path.basename(self.root_directory))
        return f"{name[0].upper()}{name[1:]}"

    def initialize(self, template_name: str):
        # Find the template to use for the new project.
        template = ProjectTemplate.find(template_name)
        template.context["project"] = self

        # Create the project directory.
        os.mkdir(self.root_directory)

        # Create empty ".cppfug" marker file.
        with open(os.path.join(self.root_directory, ".cppfug"), "w"):
            pass

        # Initialize git repository.
        pygit2.init_repository(self.root_directory)

        # Install the template.
        template.install(self.root_directory)

        # TODO: Create initial commit.
