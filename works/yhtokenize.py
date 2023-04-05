import io
import re

from PyPDF2 import PdfReader
import MeCab
import ipadic


_TAGGER = MeCab.Tagger(ipadic.MECAB_ARGS)


def extract(pdf: bytes) -> str:
    bio = io.BytesIO(pdf)
    reader = PdfReader(bio)
    texts = [
        re.sub(r"\s+", "", page.extract_text())
        for page in reader.pages
    ]
    return "\n\n".join(texts)


def parse(s: str) -> list[str]:
    ret = _TAGGER.parse(s)
    return [x.split("\t")[0] for x in ret.split("\n")]
