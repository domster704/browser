SPACE_CHARS = "\t\n\f "

CHARACTER_REFERENCE = {
    "lt": "<",
    "gt": ">",
    "amp": "&",
    "quot": '"',
    "apos": "'",
    "nbsp": " ",
    "copy": "©",
    "reg": "®",
}


def _is_ascii_alphabet(char: str) -> bool:
    return "a" <= char <= "z" or "A" <= char <= "Z"
