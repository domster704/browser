SPACE_CHARS = "\t\n\f "


def _is_ascii_alphabet(char: str) -> bool:
    return "a" <= char <= "z" or "A" <= char <= "Z"
