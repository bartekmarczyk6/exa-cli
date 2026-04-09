import os
import sys
import click
from .commands.search import search
from .commands.find_similar import find_similar
from .commands.contents import contents
from .commands.answer import answer
from .commands.research import research
from .commands.auth import auth

@click.group(invoke_without_command=True)
@click.option("--api-key", envvar="EXA_API_KEY", help="Exa API Key")
@click.pass_context
def cli(ctx, api_key):
    """Exa CLI - Search, Answer, and Research using Exa API"""
    ctx.ensure_object(dict)
    ctx.obj['API_KEY'] = api_key
    if ctx.invoked_subcommand is None:
        exe = sys.argv[0].replace(os.path.expanduser("~"), "~")
        print(f"bin: {exe}")
        print("description: Search, answer, and research using the Exa API")
        print("")
        print("commands[5]{name,description}:")
        print("  search,Neural web search")
        print("  answer,Answer a question with cited sources")
        print("  contents,Fetch contents of specific URLs")
        print("  find-similar,Find pages similar to a URL")
        print("  research,Create and poll async research tasks")
        print("")
        print("help[3]:")
        print("  Run `exa search <query>` to search the web")
        print("  Run `exa answer <question>` to get a cited answer")
        print("  Run `exa <command> --help` for command-specific options")

cli.add_command(search)
cli.add_command(find_similar)
cli.add_command(contents)
cli.add_command(answer)
cli.add_command(research)
cli.add_command(auth)

if __name__ == "__main__":
    cli()
