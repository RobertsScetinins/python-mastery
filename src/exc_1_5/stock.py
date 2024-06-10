import csv


class Stock:
    types = (str, int, float)

    def __init__(self, name: str, shares: int, price: float):
        self.name = name
        self.shares = shares
        self.price = price

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls.types, row)]
        return cls(*values)

    def cost(self):
        return self.shares * self.price

    def sell(self, shares):
        self.shares -= shares


def read_portfolio(filepath: str, data_object: object) -> list[Stock]:
    if not hasattr(data_object, "from_row"):
        raise ValueError("Wrong object provided. No 'from_row' class method found.")
    data_records = []
    with open(filepath) as file:
        csv_file = csv.reader(file)
        next(csv_file)
        for row in csv_file:
            data = data_object.from_row(row)
            data_records.append(data)
    return data_records


def print_portfolio(stocks: list[Stock]) -> None:
    print('%10s %10s %10s' % ("name", "shares", "price"))
    print(('-'*10 + ' ')*3)
    for stock in stocks:
        print(f"{stock.name:>10} {stock.shares:10d} {stock.price:10.2f}")
