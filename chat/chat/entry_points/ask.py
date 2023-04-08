import click

from ..prompt import ask2chatgpt


@click.argument("question", type=str)
@click.option("--num-context", type=int, default=5)
def ask(question: str, num_context: int):
    comp = ask2chatgpt(question, num_context)
    msg = comp.choices[0].message["content"]  # type: ignore
    print(msg)
