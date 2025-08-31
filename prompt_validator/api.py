import os
from .validators import check_prompt

import os
from prompt_validator.validators import check_prompt

def validate_directory(directory: str) -> dict:
    """
    Validate all prompts in a directory.
    Returns dict { filename: [issues] }
    """
    results = {}
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            with open(os.path.join(directory, file)) as f:
                text = f.read()
            results[file] = check_prompt(text)
    return results
