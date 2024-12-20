# import click
# from pathlib import Path
# from monopy.init.installation import DependencyInstaller

# @click.group()
# def cli():
#     """Command-line interface for managing services and utilities."""
#     pass

# @cli.command()
# @click.argument("service_or_util")
# @click.argument("name", required=False)
# @click.argument("project_dir", required=False)
# def run(service_or_util, name, project_dir):
#     """
#     Run a specific service or utility.

#     SERVICE_OR_UTIL: Specify 'service' or 'util'.
#     NAME: Name of the service or utility to run.
#     PROJECT_DIR: Directory containing `config.json`.
#     """
#     # Resolve the project directory, default to the current working directory if not provided
#     project_root = Path(project_dir).resolve() if project_dir else Path.cwd()
#     target = f"{service_or_util}s/{name}" if name else "all"

#     click.echo(f"Processing target: {target} in project: {project_root}")

#     try:
#         # Initialize and execute the DependencyInstaller
#         args = "local-case"   # can be local-case, ci-case, build-case, docker-case
#         installer = DependencyInstaller(target, project_root=project_root)
#         installer.run(args)
#     except Exception as e:
#         click.echo(f"Error: {e}", err=True)
# # !
# if __name__ == "__main__":
#     cli()

import click
from pathlib import Path
from monopylib.init.installation import DependencyInstaller


@click.group()
def cli():
    """Command-line interface for managing services and utilities."""
    pass


@cli.command()
@click.argument("service_or_util", type=click.Choice(["service", "util"], case_sensitive=False))
@click.argument("name", required=False)
@click.argument("project_dir", required=False)
@click.argument("args", default="local-case", required=False)
def run(service_or_util, name, project_dir, args):
    """
    Run a specific service or utility.

    SERVICE_OR_UTIL: Specify 'service' or 'util'.
    NAME: Name of the service or utility to run.
    PROJECT_DIR: Directory containing `config.json`.
    ARGS: Execution mode (e.g., local-case, ci-case, build-case, docker-case).
          Defaults to 'local-case' if not specified.
    """
    # Resolve the project directory, default to the current working directory if not provided
    project_root = Path(project_dir).resolve() if project_dir else Path.cwd()
    target = f"{service_or_util}s/{name}" if name else "all"

    click.echo(f"Processing target: {target} in project: {project_root}")
    click.echo(f"Execution mode: {args}")

    try:
        # Initialize and execute the DependencyInstaller
        installer = DependencyInstaller(target, project_root=project_root)
        installer.run(args)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


if __name__ == "__main__":
    cli()
