import click
import os
from datetime import datetime, timedelta

from .client import FootballDataClient
from .config import FBD_ENV_VAR
from .display import LeagueDashboard
from .leagues import SUPPORTED_LEAGUES, DEFAULT_LEAGUE
from . import __version__

# TODO: should move this logic so user can use --help without the API key
api_key = os.getenv(FBD_ENV_VAR)
if not api_key:
    # TODO: fail more gracefully
    raise ValueError(
        f"API key not found. Please set the {FBD_ENV_VAR} environment variable."
    )

dashboard = LeagueDashboard()


@click.group(invoke_without_command=True)
@click.version_option(__version__)
@click.pass_context
def cli(ctx):
    """
    Command line tool for displaying live soccer scores and statistics.
    """
    if not ctx.invoked_subcommand:
        click.echo("No subcommand provided. Use --help for available commands.")


@cli.command()
@click.option("--league", "-l", default=DEFAULT_LEAGUE, help="League code.")
def today(league):
    """
    Live scores, results, and start times for today's matches.
    """
    if league in SUPPORTED_LEAGUES.keys():
        fbd_api = FootballDataClient(api_key)
        today = datetime.now().strftime("%Y-%m-%d")
        df, _ = fbd_api.get_matches(start_date=today, end_date=today, league=league)

        dashboard.today(league, df)
    else:
        click.echo(f"League code {league} is not supported.")


@cli.command()
@click.option("--league", "-l", default=DEFAULT_LEAGUE, help="League code")
@click.option("--days", "-d", default=7, help="Days in future.")
def schedule(league, days):
    """
    Scheduled matches after today. Defaults to next 7 days.
    """
    if league in SUPPORTED_LEAGUES.keys():
        fbd_api = FootballDataClient(api_key)
        now = datetime.now()
        start_date = now.strftime("%Y-%m-%d")
        end_date = (now + timedelta(days=days)).strftime("%Y-%m-%d")
        df, _ = fbd_api.get_matches(
            start_date=start_date, end_date=end_date, league=league
        )

        dashboard.schedule(league, df)
    else:
        click.echo(f"League code {league} is not supported.")


@cli.command()
@click.option("--league", "-l", default=DEFAULT_LEAGUE, help="")
def standings(league):
    """
    Current standings for the league.
    """
    if league in SUPPORTED_LEAGUES.keys():
        fbd_api = FootballDataClient(api_key)
        df, metadata = fbd_api.get_standings(league=league)

        dashboard.standings(league, df, metadata=metadata)
    else:
        click.echo(f"League code {league} is not supported.")


@cli.command()
def leagues():
    """
    Supported leagues and their codes.
    """
    dashboard.leagues()


if __name__ == "__main__":
    cli()
