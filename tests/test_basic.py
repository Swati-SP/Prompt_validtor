import pytest
from prompt_validator.validators import check_prompt

def test_sample_prompt_runs():
    sample = "Task: Write a short poem\nSuccess Criteria: Should rhyme"
    result = check_prompt(sample)
    # Just check if function runs and returns a list
    assert isinstance(result, list)
