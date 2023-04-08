import click

from ..prompt import ask2chatgpt


@click.argument("question", type=str)
def ask(question: str):
    comp = ask2chatgpt(question)
    msg = comp.choices[0].message["content"]  # type: ignore
    print(msg)
