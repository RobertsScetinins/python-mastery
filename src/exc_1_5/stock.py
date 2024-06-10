import csv


class Stock:
    _types = (str, int, float)
    __slots__ = ("name", "_shares", "_price")

    def __init__(self, name: str, shares: int, price: float):
        self.name = name
        self._shares = shares
        self._price = price

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types, row)]
        return cls(*values)

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, value):
        if not isinstance(value, self._types[1]):
            raise TypeError(f"Expected {self._types[1].__name__}")
        if value < 0:
            raise ValueError("shares must be >= 0")
        self._shares = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, self._types[2]):
            raise TypeError(f"Expected {self._types[2].__name__}")
        if value < 0:
            raise ValueError("price must be >= 0")
        self._price = value

    @property
    def cost(self) -> float:
        return self._shares * self._price

    def sell(self, shares):
        self._shares -= shares


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
        print(f"{stock.name:>10} {stock._shares:10d} {stock._price:10.2f}")
