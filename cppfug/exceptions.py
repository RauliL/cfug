import os

from click import ClickException


class CppFugError(ClickException):
    """
    Base class for all CppFug related exceptions.
    """


class ProjectNotFoundError(CppFugError):
    """
    Exception that is thrown when user runs the `cppfug` command in a directory
    that doesn't look like to be a CppFug project.
    """

    def __init__(self):
        super().__init__(
            f"Could not find a '.cppfug' file in '{os.path.realname('.')}' or it's parent directories."
        )


class ProjectNotConfiguredError(CppFugError):
    """
    Exception that is thrown when user attempts to run CMake commands on a
    project that hasn't been configured yet.
    """

    def __init__(self):
        super().__init__(
            "Project has not been configured yet. Please run `cppfug configure` first."
        )


class TemplateDoesNotExistError(CppFugError):
    """
    Exception that is thrown when user attempts to initialize an project with
    a template that does not exist.
    """

    def __init__(self, template_name: str):
        super().__init__(f"Template does not exist: {template_name}")
