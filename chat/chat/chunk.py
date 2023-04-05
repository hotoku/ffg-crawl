from collections import deque


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
    pass
