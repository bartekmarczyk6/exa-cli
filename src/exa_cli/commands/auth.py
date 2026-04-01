import click
from ..config import load_config, save_config, get_api_key

@click.group()
def auth():
    """Authentication commands."""
    pass

@auth.command()
def login():
    """Log in to Exa by saving your API key."""
    api_key = click.prompt("Please enter your Exa API key", hide_input=True)
    config = load_config()
    config["api_key"] = api_key
    save_config(config)
    click.secho("API key saved successfully to ~/.exa/config.json", fg="green")

@auth.command()
@click.pass_context
def status(ctx):
    """Check authentication status."""
    api_key = get_api_key(ctx.obj.get('API_KEY'))
    if api_key:
        masked_key = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "***"
        click.secho(f"Logged in. API Key: {masked_key}", fg="green")
    else:
        click.secho("Not logged in. Run 'exa auth login' or set EXA_API_KEY environment variable.", fg="yellow")
