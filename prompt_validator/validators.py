import os
import json
import re
from langchain_groq import ChatGroq

# Initialize Groq LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",   # or "llama-3.1-8b-instant"
    temperature=0.7
)

def check_prompt(text: str):
    """Send prompt text to LLM and return validation issues."""
    issues = []

    # Rule 1: Check if "Task" is present
    if "Task:" not in text:
        issues.append({
            "issue": "Missing Task",
            "suggestion": "Add a clear 'Task:' section to describe the objective."
        })

    # Rule 2: Check if "Success Criteria" is present
    if "Success Criteria:" not in text:
        issues.append({
            "issue": "Missing Success Criteria",
            "suggestion": "Add 'Success Criteria:' to define measurable goals."
        })

    #  Rule 3: Check if "Examples" are present
    if "Examples:" not in text:
        issues.append({
            "issue": "Missing Examples",
            "suggestion": "Provide examples, including at least one edge case."
        })

    # Rule 4: Check for PII (emails, phone numbers)
    if re.search(r"\b\d{10}\b", text) or re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text):
        issues.append({
            "issue": "Potential PII detected",
            "suggestion": "Remove personal information such as phone numbers or emails."
        })

    # Rule 5: Check for CoT/TOT (Chain of Thought / Tree of Thought)
    if any(keyword in text.lower() for keyword in ["reason step by step", "chain of thought", "tree of thought"]):
        pass  # Already present
    else:
        issues.append({
            "issue": "Missing CoT/TOT guidance",
            "suggestion": "For complex reasoning, include 'Chain of Thought' or 'Tree of Thought' guidance."
        })

    #  Call LLM to analyze semantic issues like redundancy/conflicts
    prompt = f"Here is the prompt:\n\n{text}\n\nCheck for redundancy, conflicts, clarity, specificity, and missing parts."
    response = llm.invoke(prompt)
    content = response.content.strip()

    # Clean JSON if LLM wraps in ```json
    content = re.sub(r"^```json|```$", "", content, flags=re.MULTILINE).strip()

    try:
        model_issues = json.loads(content)
        issues.extend(model_issues)
    except Exception:
        issues.append({
            "issue": "ParsingError",
            "suggestion": content
        })

    return issues
