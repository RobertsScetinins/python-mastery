
from typing import Sequence


def print_table(data: list[Sequence], attrs: list[str]) -> None:
    print("".join(f"{col:>10}" for col in attrs))
    print(("-"*10 + " ")*len(attrs))
    for record in data:
        records_to_print = [f"{getattr(record, col):>10}" for col in attrs]
        print("".join(records_to_print))
