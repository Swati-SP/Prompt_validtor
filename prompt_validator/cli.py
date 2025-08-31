import typer
from prompt_validator.api import validate_directory
from prompt_validator.report import print_report, save_json_report

def main(
    path: str = typer.Option(..., "--path", "-p", help="Path to the folder with prompt .txt files"),
    json_output: bool = typer.Option(False, "--json-output", "-j", help="Save results to report.json"),
):
    """Validate all prompt files in a directory."""
    typer.echo(f"📂 Validating prompts in: {path}")

    results = validate_directory(path)

    if json_output:
        save_json_report(results)
        typer.echo("✅ JSON report saved as report.json")
    else:
        print_report(results)

if __name__ == "__main__":
    typer.run(main)
