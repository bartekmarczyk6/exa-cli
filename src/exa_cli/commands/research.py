import click
import time
from ..client import ExaClient
from ..config import get_api_key
from ..formatters import output_results, print_error
from .search import parse_schema

@click.group()
def research():
    """Exa Research API commands."""
    pass

@research.command()
@click.argument("instructions")
@click.option("--model", type=click.Choice(["exa-research", "exa-research-pro"]), default="exa-research")
@click.option("--output-schema")
@click.option("--poll", is_flag=True, help="Wait for completion")
@click.option("-o", "--output", type=click.Choice(["json", "table", "toon"]), default="toon")
@click.pass_context
def create(ctx, instructions, model, output_schema, poll, output):
    """Create a research task."""
    api_key = get_api_key(ctx.obj.get('API_KEY'))
    if not api_key:
        print_error("API key required", fix="Set EXA_API_KEY env var or pass --api-key <key>")
        raise SystemExit(1)

    client = ExaClient(api_key)
    
    payload = {
        "instructions": instructions,
        "model": model,
    }
    if output_schema:
        payload["outputSchema"] = parse_schema(output_schema)
        
    data = client.post("/research/v0/tasks", json=payload)
    
    if poll:
        task_id = data.get("id")
        click.secho(f"Task created: {task_id}. Polling for completion...", fg="yellow")
        while True:
            status_data = client.get(f"/research/v0/tasks/{task_id}")
            if status_data.get("status") in ("completed", "failed"):
                output_results(status_data, output, command_type="research")
                break
            time.sleep(5)
    else:
        output_results(data, output, command_type="research")

@research.command()
@click.argument("task_id")
@click.option("-o", "--output", type=click.Choice(["json", "table", "toon"]), default="toon")
@click.pass_context
def get(ctx, task_id, output):
    """Get status of a research task."""
    api_key = get_api_key(ctx.obj.get('API_KEY'))
    if not api_key:
        print_error("API key required", fix="Set EXA_API_KEY env var or pass --api-key <key>")
        raise SystemExit(1)

    client = ExaClient(api_key)
    data = client.get(f"/research/v0/tasks/{task_id}")
    output_results(data, output, command_type="research")
