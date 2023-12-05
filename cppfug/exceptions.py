class CppFugError(Exception):
    """
    Base class for all CppFug related exceptions.
    """


class TemplateDoesNotExistError(CppFugError):
    """
    Exception that is thrown when user attempts to initialize an project with
    a template that does not exist.
    """

    def __init__(self, template_name: str):
        super().__init__(f"Template does not exist: {template_name}")
