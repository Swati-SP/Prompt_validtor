from rich.table import Table
from rich.console import Console
import json

console = Console()

def print_report(file_results: dict):
    """Print CLI table for validation results"""
    table = Table(title="Prompt Validation Report")
    table.add_column("File")
    table.add_column("Issue")
    table.add_column("Suggestion")

    for file, issues in file_results.items():
        for issue in issues:
            table.add_row(file, issue["issue"], issue["suggestion"])

    console.print(table)

def save_json_report(file_results: dict, filename="report.json"):
    with open(filename, "w") as f:
        json.dump(file_results, f, indent=2)
