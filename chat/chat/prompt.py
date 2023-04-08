import logging
import os

import openai
import pandas as pd

from .keywords import condition
from .db import query
from .chunk import morphological_analysis

LOGGER = logging.getLogger(__name__)


def question2keywords(s: str) -> list[str]:
    ma = morphological_analysis(s)
    LOGGER.debug("形態素解析: %s", ma)
    ret = [
        w.word for w in
        ma
        if condition(w.word, w.attributes[0])
    ]
    return ret


def keywords2simirality(ws: list[str]) -> pd.DataFrame:
    words = ",".join(map(lambda w: f"'{w}'", ws))
    sql = f"""
    with temp1 as (
        select
          *
        from
          tfidfs
        where
          word in ({words})
    )
    select
      chunk_id,
      sum(tfidf) as similarity
    from
      temp1
    group by
      chunk_id
    """
    return query(sql).sort_values("similarity", ascending=False)


def keywords2simirality2(ws: list[str]) -> pd.DataFrame:
    words = ",".join(map(lambda w: f"'{w}'", ws))
    sql = f"""
    with temp1 as (
        select
          *
        from
          tcidfs
        where
          word in ({words})
    )
    select
      chunk_id,
      sum(tcidf) as similarity
    from
      temp1
    group by
      chunk_id
    """
    return query(sql).sort_values("similarity", ascending=False)


def load_content(ids: list[int]) -> list[str]:
    sql = f"""
    select
      content
    from
      chunks
    where
      id in ({",".join(map(str, ids))})
    """
    df = query(sql)
    return list(df["content"])


def make_prompt(question: str, num_context: int) -> str:
    kws = question2keywords(question)
    sim = keywords2simirality2(kws)
    sim_top = sim.head(num_context)

    LOGGER.debug("keywords: %s", kws)
    LOGGER.debug("sim: %s", sim)

    chunks = load_content(list(sim_top["chunk_id"]))

    context = "\n".join([f"{w[:300]}" for w in chunks])
    template = f"""
以下に、日本の金融機関に関する説明文があります。また、説明文に続いて、質問文があります。この説明文の情報から質問文に答えてください。
説明文
-----------
{context}
-----------
質問文
-----------
{question}
    """
    LOGGER.debug("prompt: %s", template)

    return template


def ask2chatgpt(prompt: str):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion
