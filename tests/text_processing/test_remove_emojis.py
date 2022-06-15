import pytest
from src.text_processing.remove_emojis import remove_emojis

EMOJIS = [
    "🏋️",
    "❤️",
    "💩",
]

@pytest.mark.parametrize("test_input,expected", [
    ("", ""),
    ("This contains a valid 🥳 emoji", "This contains a valid 🥳 emoji"),
    ("But contains a rejected ❤️ emoji", "But contains a rejected  emoji"),
    ("Is this the last test case? 🏋️ who cares", "Is this the last test case?  who cares")
])
def test_remove_emojis(test_input: str, expected: str):
    result = remove_emojis(test_input, EMOJIS)
    assert result == expected
