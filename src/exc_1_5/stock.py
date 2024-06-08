import csv


class Stock:
    def __init__(self, name: str, shares: int, price: float):
        self.name = name
        self.shares = shares
        self.price = price

    def cost(self):
        return self.shares * self.price

    def sell(self, shares):
        self.shares -= shares


def read_portfolio(filepath: str) -> list[Stock]:
    stock_records = []
    with open(filepath) as file:
        csv_file = csv.reader(file)
        next(csv_file)
        for row in csv_file:
            stock = Stock(row[0], int(row[1]), float(row[2]))
            stock_records.append(stock)
    return stock_records


def print_portfolio(stocks: list[Stock]) -> None:
    print('%10s %10s %10s' % ("name", "shares", "price"))
    print(('-'*10 + ' ')*3)
    for stock in stocks:
        print(f"{stock.name:>10} {stock.shares:10d} {stock.price:10.2f}")
