import os

import openai
import pandas as pd

from .keywords import condition
from .db import query
from .chunk import morphological_analysis


def question2keywords(s: str) -> list[str]:
    ret = [
        w.word for w in
        morphological_analysis(s)
        if condition(w.word, repr(w.attributes))
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


def make_prompt(question: str) -> str:
    kws = question2keywords(question)
    sim = keywords2simirality(kws)
    context = "\n".join(load_content(list(sim.head(5)["chunk_id"])))
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
    return template


def ask2chatgpt(question: str, print_answer=False):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    content = make_prompt(question)

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": content}
        ]
    )

    return completion
