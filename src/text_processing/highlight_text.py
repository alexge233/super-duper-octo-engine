from returns.pipeline import flow
from typing import Callable


class TextFragmentWithHighlights:
    is_highlighted: bool
    text: str

    def __init__(self, text: str, is_highlighted: bool):
        self.is_highlighted = is_highlighted
        self.text = text

    def __eq__(self, other: "TextFragmentWithHighlights") -> bool:
        return self.text == other.text and self.is_highlighted == other.is_highlighted

    def __str__(self):
        return f'TextFragmentWithHighlights(text="{self.text}", is_highlighted={self.is_highlighted})'


class TextWithHighlights:
    """
    Class encapsulates Text with Highlights, where:

    Attrs:
        fragments (list): is a list of Text Fragments/Words and respective Highlights.
    """

    fragments: list[TextFragmentWithHighlights]

    def __init__(self, fragments: list[TextFragmentWithHighlights]):
        self.fragments = fragments

    def __eq__(self, other: "TextWithHighlights") -> bool:
        return self.fragments == other.fragments

    def __str__(self) -> str:
        return "\n".join(
            [
                "TextWithHighlights(fragments=[",
                *[f"    {fragment}" for fragment in self.fragments],
                "])",
            ]
        )


def highlight_text(
    text: str, lowercase_words_to_highlight: list[str]
) -> TextWithHighlights:
    """
    Main logic goes here;
    Args:
        text (str): the actual text input
        lowercase_words_to_highlight (list): list of strings containing words to highlight

    Returns:
        TextwithHighlights (class): see above
    """
    if not isinstance(text, str):
        raise TypeError(f"Arg `text` not a string")

    fragments = flow(
        text,
        _tokenise_text,
        _create_word_highlighter(lowercase_words_to_highlight),
    )
    return TextWithHighlights(fragments)


def _create_word_highlighter(
    lowercase_words_to_highlight: list[str],
) -> Callable[[list[str]], list[TextFragmentWithHighlights]]:
    def word_highlighter(words: list[str]) -> list[TextFragmentWithHighlights]:
        return _highlight_words(words, lowercase_words_to_highlight)

    return word_highlighter


def _highlight_words(
    words: list[str], lowercase_words_to_highlight: list[str]
) -> list[TextFragmentWithHighlights]:
    """Highlight words that match both string value and case.

    Args:
        words: list of strings from tokenized text
        lowercase_words_to_highlight: list of strings of lowercase words to look for

    Returns:
        list of TextFragmentWithLights


    Raises:
        Nothing; I've delegated exceptions in `highlight_text`
    """
    if len(words) == 0:
        return []

    if len(lowercase_words_to_highlight) == 0:
        return [TextFragmentWithHighlights(is_highlighted=False, text=" ".join(words))]

    retvals = []
    prev_token = None

    for word in words:
        is_highlighted = False
        if word.casefold() in lowercase_words_to_highlight:
            is_highlighted = True

        if prev_token is None:
            retvals.append(
                TextFragmentWithHighlights(is_highlighted=is_highlighted, text=word)
            )

        else:
            if prev_token.lower() == word.lower():
                known = retvals[-1]
                known.text = f"{known.text} {word}"

            else:
                retvals.append(
                    TextFragmentWithHighlights(is_highlighted=is_highlighted, text=word)
                )

        prev_token = word

    return retvals


def _tokenise_text(text: str) -> list[str]:
    """Split by whitespace(s) and return a list of strings"""
    return text.split()
