import re
from PyPDF2 import PdfReader
import io


def extract(pdf: bytes) -> str:
    bio = io.BytesIO(pdf)
    reader = PdfReader(bio)
    texts = [
        re.sub(r"\s+", " ", page.extract_text())
        for page in reader.pages
    ]
    return "".join(texts)
