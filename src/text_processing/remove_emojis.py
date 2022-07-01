def remove_emojis(text: str, emojis_to_remove: list[str]) -> str:
    for emoji in emojis_to_remove:
        text = text.replace(emoji, '')
    return text
