import click
from ..client import ExaClient
from ..config import get_api_key
from ..formatters import output_results

@click.command()
@click.argument("url")
@click.option("-n", "--num-results", type=int, default=10)
@click.option("--include-domains", help="Comma-separated list")
@click.option("--exclude-domains", help="Comma-separated list")
@click.option("--start-published-date")
@click.option("--end-published-date")
@click.option("--start-crawl-date")
@click.option("--end-crawl-date")
@click.option("--include-text")
@click.option("--exclude-text")
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
def find_similar(ctx, url, num_results, include_domains, exclude_domains,
                 start_published_date, end_published_date, start_crawl_date, end_crawl_date,
                 include_text, exclude_text, text, text_max_chars, highlights, highlights_max_chars,
                 highlights_query, summary, summary_query, livecrawl, subpages, subpage_target,
                 extras_links, extras_image_links, output):
    """Find similar pages to a given URL."""
    api_key = get_api_key(ctx.obj.get('API_KEY'))
    if not api_key:
        click.secho("API key required. Set EXA_API_KEY or use --api-key.", fg="red")
        raise click.Abort()

    client = ExaClient(api_key)
    
    payload = {
        "url": url,
        "numResults": num_results
    }
    
    if include_domains: payload["includeDomains"] = include_domains.split(",")
    if exclude_domains: payload["excludeDomains"] = exclude_domains.split(",")
    if start_published_date: payload["startPublishedDate"] = start_published_date
    if end_published_date: payload["endPublishedDate"] = end_published_date
    if start_crawl_date: payload["startCrawlDate"] = start_crawl_date
    if end_crawl_date: payload["endCrawlDate"] = end_crawl_date
    if include_text: payload["includeText"] = include_text.split(",")
    if exclude_text: payload["excludeText"] = exclude_text.split(",")

    contents = {}
    if text or text_max_chars:
        contents["text"] = {"maxCharacters": text_max_chars} if text_max_chars else True
    if highlights or highlights_max_chars or highlights_query:
        h_opts = {}
        if highlights_max_chars: h_opts["maxCharacters"] = highlights_max_chars
        if highlights_query: h_opts["query"] = highlights_query
        contents["highlights"] = h_opts if h_opts else True
    if summary or summary_query:
        contents["summary"] = {"query": summary_query} if summary_query else True
    if livecrawl: contents["livecrawl"] = livecrawl
    if subpages: contents["subpages"] = subpages
    if subpage_target: contents["subpageTarget"] = subpage_target
    if extras_links or extras_image_links:
        contents["extras"] = {}
        if extras_links: contents["extras"]["links"] = extras_links
        if extras_image_links: contents["extras"]["imageLinks"] = extras_image_links

    if contents:
        payload["contents"] = contents

    data = client.post("/findSimilar", json=payload)
    output_results(data, output, command_type="find_similar", show_text=text, show_highlights=highlights)
