from .chunk import extract_keywords


def prompt(query: str) -> str:
    keywords = extract_keywords(query)
