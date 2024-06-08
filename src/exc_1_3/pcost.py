from pathlib import Path

CUR_DIR = Path(__file__).parent
DATA_DIR = CUR_DIR.parent.parent / "Data"
VALID_DATA_PATH = DATA_DIR / "portfolio.dat"
ERROR_DATA_PATH = DATA_DIR / "portfolio3.dat"


def portfolio_cost(filepath: Path) -> float:

    total = 0
    with open(filepath, "r") as file_read:
        for line in file_read:
            print(line)
            line_list = line.split()
            try:
                count = int(line_list[1])
                price = float(line_list[2])
            except ValueError as exc:
                print("Couldn't parse:", line)
                print("Reason:", exc)
            else:
                print(count)
                print(price)
                total += int(count) * float(price)
    print(total)
    return total


if __name__ == "__main__":
    print(portfolio_cost(VALID_DATA_PATH))
    # print(portfolio_cost(ERROR_DATA_PATH))
