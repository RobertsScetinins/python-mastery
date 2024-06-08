import sys
import random


CHARS = r"\|/"


def draw(rows, columns) -> None:
    for _ in range(rows):
        print("".join(random.choice(CHARS) for _ in range(columns)))
    

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: art.py rows columns")
    rows = int(sys.argv[1])
    columns = int(sys.argv[2])
    draw(rows, columns)
