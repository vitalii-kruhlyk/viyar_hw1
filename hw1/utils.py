import re
import cyrtranslit


def normalize(text: str) -> str:

    transliterated_string = cyrtranslit.to_latin(text, "ua")
    normalized_name = re.sub(r"[^a-zA-Z0-9]", "_", transliterated_string)
    return normalized_name
