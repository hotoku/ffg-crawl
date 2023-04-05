from collections import deque
import re

import MeCab
import ipadic

_TAGGER = MeCab.Tagger(ipadic.MECAB_ARGS)


def split_to_chunk(s: str, max_len: int, sep: str = "。") -> list[str]:
    sententces = deque(s.strip(sep).split(sep))
    ret: list[str] = []
    chunk_buf: list[str] = []
    while len(sententces) > 0:
        cur = sententces.popleft()
        chunk_buf.append(cur)
        if sum(map(len, chunk_buf)) >= max_len:
            ret.append(sep.join(chunk_buf) + sep)
            chunk_buf = []
            continue
    if len(chunk_buf) > 0:
        ret.append(sep.join(chunk_buf) + sep)

    return ret


def extract_keywords(s: str) -> list[str]:
    words = _TAGGER.parse(s).split("\n")
    # 最後の2個はEOSと空文字なので削除
    infos = list(map(lambda s: re.split(r"[\t,]", s), words))[:-2]
    ret: list[str] = []
    for info in infos:
        if info[1] == "名詞" and info[2] in ("一般", "固有名詞"):
            ret.append(info[7])
    return ret
