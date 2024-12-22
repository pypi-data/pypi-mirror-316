import rich
import typer

app = typer.Typer()


@app.command()
def main() -> None:
    rich.print(
        "[bold green][!][/] Mike Moran, Ph.D.",
        "[bold green][+][/] threat researcher, detection engineer, data scientist",
        "[bold blue][+][/] Material Security",
        "[bold blue][+][/] mike@mkmrn.dev",
        "[bold red][?][/] gitlab.com/mmoran0032",
        "[bold red][?][/] github.com/mmoran0032",
        "[bold red][?][/] linkedin.com/in/mmoran0032",
        sep="\n",
    )


if __name__ == "__main__":
    app()
