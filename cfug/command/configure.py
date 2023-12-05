import click

from ..project import Project


@click.command(help="Runs CMake configuration on the project.")
def configure():
    Project.find().configure()
