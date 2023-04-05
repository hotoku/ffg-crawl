from chat.chunk import split_to_chunk, extract_keywords


def test_chunk():
    max_len = 2
    s = "あああ。いいい。ううう。"
    ret = split_to_chunk(s, max_len)
    assert ret == ["あああ。", "いいい。", "ううう。"]


def test_chunk2():
    max_len = 3
    s = "あああ。いいい。ううう。"
    ret = split_to_chunk(s, max_len)
    assert ret == ["あああ。", "いいい。", "ううう。"]


def test_chunk3():
    max_len = 4
    s = "あああ。いいい。ううう。"
    ret = split_to_chunk(s, max_len)
    assert ret == ["あああ。いいい。", "ううう。"]


def test_chunk4():
    max_len = 6
    s = "あああ。いいい。ううう。"
    ret = split_to_chunk(s, max_len)
    assert ret == ["あああ。いいい。", "ううう。"]


def test_chunk5():
    max_len = 7
    s = "あああ。いいい。ううう。"
    ret = split_to_chunk(s, max_len)
    assert ret == ["あああ。いいい。ううう。"]


def test_chunk6():
    max_len = 10
    s = "あああ。いいい。ううう。"
    ret = split_to_chunk(s, max_len)
    assert ret == ["あああ。いいい。ううう。"]


def test_keywords():
    s = "吾輩は猫である"
    ret = extract_keywords(s)
    assert ret == ["猫"]
