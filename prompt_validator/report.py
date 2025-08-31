from rich.table import Table
from rich.console import Console

console = Console()

def print_report(results):
    table = Table(title="Prompt Validation Report")
    table.add_column("File")
    table.add_column("Issue")
    table.add_column("Suggestion")

    # results is a list of dicts, not a dict
    for entry in results:
        file = entry["file"]
        for issue in entry["issues"]:
            table.add_row(file, issue["issue"], issue["suggestion"])

    console.print(table)


def save_json_report(results, filename="report.json"):
    import json
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
