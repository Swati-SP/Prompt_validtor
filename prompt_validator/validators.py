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
    """Send prompt text to LLM and return validation issues as structured JSON."""
    messages = [
        {"role": "system", "content": (
            "You are a strict prompt validator. "
            "Your task: analyze the given prompt for issues. "
            "Return ONLY a JSON array, no extra text, in this format:\n"
            "[\n"
            "  {\"issue\": \"<short_issue>\", \"suggestion\": \"<fix>\"},\n"
            "  ...\n"
            "]"
        )},
        {"role": "user", "content": f"Here is the prompt:\n\n{text}"}
    ]

    response = llm.invoke(messages)
    content = response.content.strip()

    # Remove markdown fences if model adds them
    content = re.sub(r"^```json|```$", "", content, flags=re.MULTILINE).strip()

    try:
        issues = json.loads(content)
        return issues
    except Exception:
        return [{"issue": "ParsingError", "suggestion": content}]
