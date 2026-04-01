import click
import json
from ..client import ExaClient
from ..config import get_api_key
from ..formatters import output_results

@click.command()
@click.argument("query")
@click.option("--stream", is_flag=True, help="Enable SSE streaming")
@click.option("--text", is_flag=True, help="Include full text in citations")
@click.option("-o", "--output", type=click.Choice(["json", "table", "csv"]), default="table")
@click.pass_context
def answer(ctx, query, stream, text, output):
    """Answer a question using Exa."""
    api_key = get_api_key(ctx.obj.get('API_KEY'))
    if not api_key:
        click.secho("API key required. Set EXA_API_KEY or use --api-key.", fg="red")
        raise click.Abort()

    client = ExaClient(api_key)
    
    payload = {
        "query": query,
        "stream": stream,
        "text": text
    }
    
    if stream:
        for chunk in client.stream_post("/answer", json=payload):
            try:
                data = json.loads(chunk)
                if "text" in data:
                    click.echo(data["text"], nl=False)
            except Exception:
                pass
        click.echo()
    else:
        data = client.post("/answer", json=payload)
        output_results(data, output, command_type="answer")
