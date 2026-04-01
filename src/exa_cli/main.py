import click
from .commands.search import search
from .commands.find_similar import find_similar
from .commands.contents import contents
from .commands.answer import answer
from .commands.research import research
from .commands.auth import auth

@click.group()
@click.option("--api-key", envvar="EXA_API_KEY", help="Exa API Key")
@click.pass_context
def cli(ctx, api_key):
    """Exa CLI - Search, Answer, and Research using Exa API"""
    ctx.ensure_object(dict)
    ctx.obj['API_KEY'] = api_key

cli.add_command(search)
cli.add_command(find_similar)
cli.add_command(contents)
cli.add_command(answer)
cli.add_command(research)
cli.add_command(auth)

if __name__ == "__main__":
    cli()
