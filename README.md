Prompt Validator

A Python-based Prompt Validation Tool that checks AI prompts for redundancy, conflicts, completeness, and sensitive information.
Think of it as a Grammarly for AI prompts — it ensures prompts are clear, consistent, and safe before use.

Features:-

 Detects redundant instructions (repeated phrases with no added value)
 Detects conflicting instructions (e.g., “be concise” vs “write 3000 words”)
 Checks completeness (Task, Success Criteria, Examples, CoT/TOT steps)
 Flags PII or secrets (phone numbers, emails, credentials)
 Generates human-readable table report in the terminal
 Can save JSON report for further processing
 Built with Groq LLM + LangChain for deeper semantic validation

 📂 Project Structure
 prompt_validator/
│── prompt_validator/
│   ├── __init__.py
│   ├── cli.py         # Command-line interface
│   ├── api.py         # Directory scanning & orchestration
│   ├── report.py      # Reporting (table + JSON)
│   ├── validators.py  # Prompt validation logic (LLM + regex)
│── sample_prompts/    # Example prompts to test the tool
│   ├── prompt1.txt
│   ├── prompt2.txt
│   ├── prompt3.txt
│   └── prompt4.txt
│── tests/             # Unit test placeholders
│── requirements.txt   # Dependencies
│── README.md          # Project documentation

⚙️ Installation
1. Clone the repository
git clone https://github.com/Swati-SP/Prompt_validtor.git
cd prompt-validator

2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate    # On Windows
source venv/bin/activate # On Linux/Mac

3. Install dependencies
pip install -r requirements.txt

🔑 Setup API Key

On Command Prompt (cmd.exe):
set GROQ_API_KEY=gsk_your_api_key_here
On PowerShell:
$env:GROQ_API_KEY="gsk_your_api_key_here"
On Linux/Mac:
export GROQ_API_KEY="gsk_your_api_key_here"

Verify:
echo %GROQ_API_KEY%   # Windows (cmd)
echo $env:GROQ_API_KEY  # PowerShell
echo $GROQ_API_KEY    # Linux/Mac

Usage

Validate all prompts in a folder:
python -m prompt_validator.cli --path sample_prompts
Save output as JSON:
python -m prompt_validator.cli --path sample_prompts --json-output

📝 Example Output

┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ File        ┃ Issue                         ┃ Suggestion                                           ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ prompt1.txt │ Duplicate Success Criteria    │ Remove duplicate success criteria into one statement │
│ prompt2.txt │ Conflicting Instructions      │ Can't be both concise AND 3000 words, clarify        │
│ prompt3.txt │ Lack of Specificity           │ Add technical details about ATM security             │
│ prompt4.txt │ PII Violation                 │ Remove personal email/phone and use generic info     │
└─────────────┴───────────────────────────────┴──────────────────────────────────────────────────────┘

Testing
Run unit tests:
pytest --maxfail=1 --disable-warnings -q

Generate coverage report:
pytest --cov=prompt_validator







