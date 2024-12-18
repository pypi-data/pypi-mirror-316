import click

from cased.commands.build import build
from cased.commands.deploy import deploy
from cased.commands.init import init
from cased.commands.login import login, logout
from cased.commands.resources import branches, deployments, projects, targets

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group()
def cli():
    """
    Cased CLI for authentication, target setup, and branch deployment.

    Use 'cased COMMAND --help' for more information on a specific command.
    """

    pass


cli.add_command(deploy)
cli.add_command(init)
cli.add_command(build)
cli.add_command(login)
cli.add_command(logout)
cli.add_command(deployments)
cli.add_command(branches)
cli.add_command(projects)
cli.add_command(targets)


if __name__ == "__main__":
    try:
        cli()
    except Exception as _:
        click.echo("\nProcess interrupted. Exiting.")
