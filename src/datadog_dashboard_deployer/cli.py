"""
Command-line interface for the DataDog Dashboard Deployer.
"""

import os
import sys

import click

from . import __version__
from .core import DashboardDeployer
from .utils import format_error, setup_logging, validate_environment


@click.group()
@click.version_option(version=__version__)
def cli():
    """DataDog Dashboard Deployer - Deploy dashboards as code."""
    pass


@cli.command()
@click.argument("config_file", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--dry-run", is_flag=True, help="Validate configuration without deploying"
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.option("--site", help="DataDog site (e.g., datadoghq.com)")
def deploy(config_file, dry_run, verbose, site):
    """Deploy dashboards from configuration file."""
    try:
        # Set up logging
        setup_logging("DEBUG" if verbose else "INFO")

        # Validate environment
        validate_environment()

        # Get credentials from environment
        api_key = os.environ["DATADOG_API_KEY"]
        app_key = os.environ["DATADOG_APP_KEY"]

        # Initialize deployer
        deployer = DashboardDeployer(api_key, app_key, site)

        # Deploy dashboards
        result = deployer.deploy(config_file, dry_run=dry_run)

        if dry_run:
            click.echo("Dry run completed successfully. Configuration is valid.")
        else:
            click.echo("Deployment completed successfully:")
            for dashboard in result["results"]:
                click.echo(
                    f"- {dashboard['action'].title()}: {dashboard['name']} (ID: {dashboard['dashboard_id']})"
                )

    except Exception as e:
        click.echo(f"Error: {format_error(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("config_file", type=click.Path(exists=True, dir_okay=False))
def validate(config_file):
    """Validate dashboard configuration file."""
    try:
        # Set up logging
        setup_logging("INFO")

        # Initialize deployer with dummy credentials for validation
        deployer = DashboardDeployer("dummy_api_key", "dummy_app_key")

        # Validate configuration
        deployer.deploy(config_file, dry_run=True)
        click.echo("Configuration is valid.")

    except Exception as e:
        click.echo(f"Configuration is invalid: {format_error(e)}", err=True)
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    cli()
