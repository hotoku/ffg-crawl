import click

from ..prompt import ask2chatgpt, make_prompt


@click.argument("question", type=str)
@click.option("-n", "--num-context", type=int, default=5)
@click.option("--dry-run", is_flag=True)
def ask(question: str, num_context: int, dry_run: bool):
    prompt = make_prompt(question, num_context)
    if not dry_run:
        comp = ask2chatgpt(prompt)
        msg = comp.choices[0].message["content"]  # type: ignore
        print(msg)
