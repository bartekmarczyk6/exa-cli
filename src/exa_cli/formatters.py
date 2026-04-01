import json
import csv
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

def print_json(data):
    console.print_json(data=data)

def print_csv(results):
    if not results:
        return
    writer = csv.writer(sys.stdout)
    writer.writerow(["Title", "URL", "Published", "Score"])
    for res in results:
        title = res.get("title", "No Title")
        url = res.get("url", "")
        pub = res.get("publishedDate", "")[:10] if res.get("publishedDate") else ""
        score = f"{res.get('score', 0):.3f}"
        writer.writerow([title, url, pub, score])

def print_table_results(results, show_text=False, show_highlights=False):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Title", min_width=20)
    table.add_column("URL", overflow="fold")
    table.add_column("Published", justify="right")
    table.add_column("Score", justify="right")

    for i, res in enumerate(results):
        title = res.get("title", "No Title")
        url = res.get("url", "")
        pub = res.get("publishedDate", "")[:10] if res.get("publishedDate") else ""
        score = f"{res.get('score', 0):.3f}"
        table.add_row(str(i+1), title, url, pub, score)

    console.print(table)

    if show_text or show_highlights:
        for i, res in enumerate(results):
            console.print(f"\n[bold cyan]--- Result {i+1}: {res.get('title', 'No Title')} ---[/bold cyan]")
            if show_text and "text" in res:
                console.print(Panel(res["text"], title="Text", expand=False))
            if show_highlights and "highlights" in res:
                for h in res["highlights"]:
                    console.print(f"- {h}")
            if "summary" in res:
                console.print(Panel(res["summary"], title="Summary", expand=False))

def print_answer(data):
    answer = data.get("answer", "")
    console.print(Markdown(answer))
    citations = data.get("citations", [])
    if citations:
        console.print("\n[bold]Citations:[/bold]")
        for i, cit in enumerate(citations):
            console.print(f"[{i+1}] {cit.get('title', '')} - {cit.get('url', '')}")

def print_research_task(data):
    console.print(f"[bold]Task ID:[/bold] {data.get('id')}")
    console.print(f"[bold]Status:[/bold] {data.get('status')}")
    if data.get("status") == "completed":
        console.print("\n[bold]Output:[/bold]")
        console.print_json(data=data.get("output", {}))

def output_results(data, format_type, command_type="search", **kwargs):
    if format_type == "json":
        print_json(data)
        return

    if command_type in ("search", "find_similar", "contents"):
        results = data.get("results", [])
        if format_type == "csv":
            print_csv(results)
        else:
            print_table_results(results, show_text=kwargs.get("show_text"), show_highlights=kwargs.get("show_highlights"))
    elif command_type == "answer":
        print_answer(data)
    elif command_type == "research":
        print_research_task(data)
