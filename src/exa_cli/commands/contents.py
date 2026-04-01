import click
from ..client import ExaClient
from ..config import get_api_key
from ..formatters import output_results

@click.command()
@click.argument("urls", nargs=-1, required=True)
@click.option("--text", is_flag=True)
@click.option("--text-max-chars", type=int)
@click.option("--highlights", is_flag=True)
@click.option("--highlights-max-chars", type=int)
@click.option("--highlights-query")
@click.option("--summary", is_flag=True)
@click.option("--summary-query")
@click.option("--livecrawl", type=click.Choice(["never", "fallback", "always", "auto", "preferred"]))
@click.option("--subpages", type=int)
@click.option("--subpage-target")
@click.option("--extras-links", type=int)
@click.option("--extras-image-links", type=int)
@click.option("-o", "--output", type=click.Choice(["json", "table", "csv"]), default="table")
@click.pass_context
def contents(ctx, urls, text, text_max_chars, highlights, highlights_max_chars,
             highlights_query, summary, summary_query, livecrawl, subpages, subpage_target,
             extras_links, extras_image_links, output):
    """Get contents of specific URLs."""
    api_key = get_api_key(ctx.obj.get('API_KEY'))
    if not api_key:
        click.secho("API key required. Set EXA_API_KEY or use --api-key.", fg="red")
        raise click.Abort()

    client = ExaClient(api_key)
    
    payload = {
        "urls": list(urls)
    }
    
    if text or text_max_chars:
        payload["text"] = {"maxCharacters": text_max_chars} if text_max_chars else True
    if highlights or highlights_max_chars or highlights_query:
        h_opts = {}
        if highlights_max_chars: h_opts["maxCharacters"] = highlights_max_chars
        if highlights_query: h_opts["query"] = highlights_query
        payload["highlights"] = h_opts if h_opts else True
    if summary or summary_query:
        payload["summary"] = {"query": summary_query} if summary_query else True
    if livecrawl: payload["livecrawl"] = livecrawl
    if subpages: payload["subpages"] = subpages
    if subpage_target: payload["subpageTarget"] = subpage_target
    if extras_links or extras_image_links:
        payload["extras"] = {}
        if extras_links: payload["extras"]["links"] = extras_links
        if extras_image_links: payload["extras"]["imageLinks"] = extras_image_links

    data = client.post("/contents", json=payload)
    output_results(data, output, command_type="contents", show_text=text, show_highlights=highlights)
