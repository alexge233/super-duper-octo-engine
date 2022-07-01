import pytest
from src.text_processing.highlight_text import (
    highlight_text,
    TextFragmentWithHighlights,
    TextWithHighlights,
)


def test_empty_text():
    result = highlight_text("", [])
    assert result == TextWithHighlights([])


def test_text_with_empty_words():
    message = "This is a test message to test the message highlighter."
    result = highlight_text(message, [])

    assert result == TextWithHighlights([
        TextFragmentWithHighlights(message, is_highlighted=False)
    ])


def test_text_with_multiple_spaces():
    message = "This message has   multiple  spaces between  words."
    result = highlight_text(message, [])
    assert result == TextWithHighlights([
        TextFragmentWithHighlights("This message has multiple spaces between words.", is_highlighted=False),
    ])


def test_different_case_words():
    message = "Hello hello HeLLo HELLO"
    result = highlight_text(message, ["hello"])
    assert result == TextWithHighlights([
        TextFragmentWithHighlights(message, is_highlighted=True),
    ])


def test_words_in_multiple_groups():
    message = "Hello World! hello world! HeLLo WoRlD! HELLO WORLD!"
    result = highlight_text(message, ["hello"])
    assert result == TextWithHighlights([
        TextFragmentWithHighlights("Hello", is_highlighted=True),
        TextFragmentWithHighlights("World!", is_highlighted=False),
        TextFragmentWithHighlights("hello", is_highlighted=True),
        TextFragmentWithHighlights("world!", is_highlighted=False),
        TextFragmentWithHighlights("HeLLo", is_highlighted=True),
        TextFragmentWithHighlights("WoRlD!", is_highlighted=False),
        TextFragmentWithHighlights("HELLO", is_highlighted=True),
        TextFragmentWithHighlights("WORLD!", is_highlighted=False),
    ])


def test_malformed_args():
    with pytest.raises(TypeError):
        highlight_text(None, [])

    with pytest.raises(TypeError):
        highlight_text(49, ['hello'])


def test_multigroup_multiword():
    message = "Hello World! Hello hello"
    result  = highlight_text(message, ["hello"])

    assert result == TextWithHighlights(fragments=[
        TextFragmentWithHighlights(text="Hello", is_highlighted=True),
        TextFragmentWithHighlights(text="World!", is_highlighted=False),
        TextFragmentWithHighlights(text="Hello hello", is_highlighted=True)
    ])


def test_mixed_argtypes():
    message = "Hello 49, what's your mission?"
    result  = highlight_text(message, [49])

    assert result == TextWithHighlights(fragments=[
        TextFragmentWithHighlights(text="Hello", is_highlighted=False),
        TextFragmentWithHighlights(text="49,", is_highlighted=False),
        TextFragmentWithHighlights(text="what's", is_highlighted=False),
        TextFragmentWithHighlights(text="your", is_highlighted=False),
        TextFragmentWithHighlights(text="mission?", is_highlighted=False)
    ])
