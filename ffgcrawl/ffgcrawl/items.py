from dataclasses import dataclass


@dataclass
class PdfItem:
    url: str
    content: bytes

@dataclass
class TextItem:
    url: str
    title: str
    content: str
