import typer

app = typer.Typer()

@app.command()
def generate(ids: str):
    """Placeholder generator CLI that would request IDs from API and render PDFs."""
    typer.echo(f"Would generate PDFs for ids: {ids}")

if __name__ == "__main__":
    app()
