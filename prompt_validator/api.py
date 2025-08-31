import os
from .validators import check_prompt

def validate_directory(path: str, fix: bool = False):
    results = []
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            filepath = os.path.join(path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

            issues = check_prompt(text)

            # If fix enabled → auto-update
            if fix and issues:
                fixed_text = apply_fixes(text, issues)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(fixed_text)

            results.append({"file": filename, "issues": issues})
    return results


def apply_fixes(text: str, issues: list) -> str:
    """Very basic auto-fix: just appends missing sections or removes PII."""
    for issue in issues:
        if issue["issue"] == "Missing Task":
            text = "Task: [Add task here]\n" + text
        elif issue["issue"] == "Missing Success Criteria":
            text += "\n\nSuccess Criteria: [Add measurable criteria here]"
        elif issue["issue"] == "Missing Examples":
            text += "\n\nExamples: [Add at least one example + one edge case]"
        elif issue["issue"] == "Potential PII detected":
            # remove emails and phone numbers
            import re
            text = re.sub(r"\b\d{10}\b", "[REDACTED]", text)
            text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[REDACTED]", text)
        elif issue["issue"] == "Missing CoT/TOT guidance":
            text += "\n\nGuidance: Use Chain of Thought reasoning for complex steps."

    return text
