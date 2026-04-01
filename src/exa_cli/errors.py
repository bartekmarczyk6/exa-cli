import click

def handle_api_error(response):
    status = response.status_code
    try:
        data = response.json()
        error_msg = data.get("error", "Unknown error")
        tag = data.get("tag", "")
    except Exception:
        error_msg = response.text
        tag = ""

    if status == 401:
        click.secho("Invalid API key. Set EXA_API_KEY or use --api-key.", fg="red")
    elif status == 402:
        click.secho("Out of credits. Visit dashboard.exa.ai.", fg="red")
    elif status == 429:
        click.secho("Rate limited. Retrying...", fg="yellow")
    elif status == 400:
        click.secho(f"Validation Error: {error_msg} (Tag: {tag})", fg="red")
    elif status >= 500:
        click.secho(f"Server error ({status}). Retrying...", fg="red")
    else:
        click.secho(f"API Error {status}: {error_msg}", fg="red")
    
    raise click.Abort()
