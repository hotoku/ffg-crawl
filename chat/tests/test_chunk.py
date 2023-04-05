from chat.chunk import split_to_chunk


def test_chunk():
    max_len = 2
    s = "あああ。いいい。ううう。"
    ret = split_to_chunk(s, max_len)
    assert ret == ["あああ。", "いいい。", "ううう。"]


def test_chun2():
    max_len = 3
    s = "あああ。いいい。ううう。"
    ret = split_to_chunk(s, max_len)
    assert ret == ["あああ。", "いいい。", "ううう。"]


def test_chun3():
    max_len = 4
    s = "あああ。いいい。ううう。"
    ret = split_to_chunk(s, max_len)
    assert ret == ["あああ。いいい。", "ううう。"]


def test_chun4():
    max_len = 6
    s = "あああ。いいい。ううう。"
    ret = split_to_chunk(s, max_len)
    assert ret == ["あああ。いいい。", "ううう。"]


def test_chun5():
    max_len = 7
    s = "あああ。いいい。ううう。"
    ret = split_to_chunk(s, max_len)
    assert ret == ["あああ。いいい。ううう。"]


def test_chun6():
    max_len = 10
    s = "あああ。いいい。ううう。"
    ret = split_to_chunk(s, max_len)
    assert ret == ["あああ。いいい。ううう。"]
