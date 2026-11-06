import json
from pathlib import Path

import pytest

from app.guardrails import validate_input


BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "datasets" / "adversarial_prompts.json"

with open(DATASET_PATH, "r", encoding="utf-8") as file:
    adversarial_prompts = json.load(file)


@pytest.mark.parametrize("prompt", adversarial_prompts)
def test_prompt_injection_is_blocked(prompt):
    is_valid, message = validate_input(prompt)

    assert is_valid is False
    assert message == "Potential prompt injection detected."


def test_normal_prompt_is_allowed():
    is_valid, message = validate_input(
        "Explain retrieval augmented generation."
    )

    assert is_valid is True


def test_empty_prompt_is_blocked():
    is_valid, message = validate_input("")

    assert is_valid is False


def test_oversized_prompt_is_blocked():
    is_valid, message = validate_input("A" * 5001)

    assert is_valid is False