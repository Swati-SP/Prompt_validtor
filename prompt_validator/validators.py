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

    # Rule 3: Check if "Examples" are present
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
    if not any(keyword in text.lower() for keyword in ["reason step by step", "chain of thought", "tree of thought"]):
        issues.append({
            "issue": "Missing CoT/TOT guidance",
            "suggestion": "For complex reasoning, include 'Chain of Thought' or 'Tree of Thought' guidance."
        })

    # --- Call LLM to analyze semantic issues ---
    prompt = f"""
You are a strict JSON validator. Analyze the following prompt:

{text}

Return ONLY a valid JSON list of objects. 
Each object must have two fields: "issue" and "suggestion".
Example:
[
  {{
    "issue": "Redundancy",
    "suggestion": "Remove duplicate success criteria."
  }}
]

Do not include explanations, markdown, or extra text.
"""
    response = llm.invoke(prompt)
    content = response.content.strip()

    # Try to extract JSON only (if model added extra text)
    content = re.sub(r"^```json|```$", "", content, flags=re.MULTILINE).strip()
    content = re.search(r"\[.*\]", content, flags=re.DOTALL)
    if content:
        content = content.group(0)

    try:
        model_issues = json.loads(content)
        issues.extend(model_issues)
    except Exception:
        issues.append({
            "issue": "ParsingError",
            "suggestion": response.content.strip()
        })

    return issues
