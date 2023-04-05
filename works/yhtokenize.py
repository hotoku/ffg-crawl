import io
import re

from PyPDF2 import PdfReader
import MeCab
import ipadic


_TAGGER = MeCab.Tagger(ipadic.MECAB_ARGS)
_SEP = re.compile("[\t,]")


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
    words = [_SEP.split(x) for x in ret.split("\n")]
    words2 = words[:-1]  # 最後は空文字なので消す
    words3, eos = words2[:-1], words2[-1]  # EOSが最後の要素
    return [w[7] for w in words3 if w[7] != "*"] + eos  # 未知語は*なので削除
