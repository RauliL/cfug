import os
import pytest

from pathlib import Path

from ..project import Project


@pytest.mark.parametrize(
    ("root_directory", "expected_result"),
    (("awesome-project", "AwesomeProject"), ("test", "Test"), ("foo_bar", "FooBar")),
)
def test_name(root_directory: str, expected_result: str):
    project = Project(root_directory=Path(root_directory))

    assert project.name == expected_result


def test_build_directory():
    project = Project(root_directory=Path(os.path.join("foo", "bar")))

    assert project.build_directory == Path(os.path.join("foo", "bar", "build"))
