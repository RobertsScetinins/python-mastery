import collections
import collections.abc
import csv
from pathlib import Path

CURRENT_DIR = Path(__file__).parent
DATA_DIR = CURRENT_DIR.parent.parent / "Data/ctabus.csv"


class RideData(collections.abc.Sequence):
    def __init__(self) -> None:
        self.routes = []
        self.dates = []
        self.daytypes = []
        self.numrides = []
    
    def __len__(self):
        return len(self.routes)
    
    def __getitem__(self, index) -> dict:

        routes = self.routes[index]
        dates = self.dates[index]
        daytypes = self.daytypes[index]
        numrides = self.numrides[index]
        if len(routes) == 1:
            return dict(
                route=routes,
                date=dates,
                daytype=daytypes,
                rides=numrides
            )
        else:
            rows = []
            for i in range(len(routes)):
                rows.append(
                    dict(
                        route=routes[i],
                        date=dates[i],
                        daytype=daytypes[i],
                        rides=numrides[i]
                    )
                )
            return rows
    
    def append(self, d: dict):
        self.routes.append(d["route"])
        self.dates.append(d["date"])
        self.daytypes.append(d["daytype"])
        self.numrides.append(d["rides"])


def read_rides_as_tuples(filename: str) -> list[tuple]:
    """Read the bus ride data as a list of tuples."""
    print("")
    records = []
    with open(filename) as file:
        rows = csv.reader(file)
        next(rows)  # skip header
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = route, date, daytype, rides
            records.append(record)
    return records


def read_rides_as_dict(filename: str) -> list[dict]:  # the worst efficient storage
    """Read the bus ride data as a list of dict."""

    records = RideData()
    with open(filename) as file:
        rows = csv.reader(file)
        next(rows)  # skip header
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = {
                "route": route,
                "date": date,
                "daytype": daytype,
                "rides": rides,
            }
            records.append(record)
    return records


def read_rides_as_class(filename: str) -> list:
    """Read the bus ride data as a list of class instances."""

    class Record:
        def __init__(self, route: str, date: str, daytype: str, rides: int):
            self.route = route
            self.date = date
            self.daytype = daytype
            self.rides = rides

    records = []
    with open(filename) as file:
        rows = csv.reader(file)
        next(rows)  # skip header
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = Record(route, date, daytype, rides)
            records.append(record)
    return records


def read_rides_as_named_tuple(filename: str) -> list:
    """Read the bus ride data as a list of named tuples."""
    from collections import namedtuple
    Record = namedtuple("Record", ["route", "date", "daytype", "rides"])

    records = []
    with open(filename) as file:
        rows = csv.reader(file)
        next(rows)  # skip header
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = Record(route=route, date=date, daytype=daytype, rides=rides)
            records.append(record)
    return records


def read_rides_as_slots_class(filename: str) -> list:  # the most efficient storage
    """Read the bus ride data as a list of Record instances with slots."""

    class Record:
        __slots__ = ["route", "date", "daytype", "rides"]

        def __init__(self, route: str, date: str, daytype: str, rides: int):
            self.route = route
            self.date = date
            self.daytype = daytype
            self.rides = rides

    records = []
    with open(filename) as file:
        rows = csv.reader(file)
        next(rows)  # skip header
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = Record(route, date, daytype, rides)
            records.append(record)
    return records


def read_rides_as_data_class(filename: str) -> list:
    """Read the bus ride data as a list of Record instances with slots."""

    from dataclasses import dataclass

    @dataclass
    class Record:
        route: str
        date: str
        daytype: str
        rides: int

    records = []
    with open(filename) as file:
        rows = csv.reader(file)
        next(rows)  # skip header
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = Record(route, date, daytype, rides)
            records.append(record)
    return records


def read_rides_as_columns(filename: str) -> list:
    # more efficient than dicts because less memory alloc for 4 lists instead of thousands dicts
    """Read the bus ride data as a list of Record instances with slots."""

    routes = []
    dates = []
    daytypes = []
    numrides = []

    with open(filename) as file:
        rows = csv.reader(file)
        next(rows)  # skip header
        for row in rows:
            routes.append(row[0])
            dates.append(row[1])
            daytypes.append(row[2])
            numrides.append(int(row[3]))
    return dict(routes=routes, dates=dates, daytypes=daytypes, numrides=numrides)


if __name__ == "__main__":
    import tracemalloc
    tracemalloc.start()

    func = read_rides_as_dict
    print(func.__name__)
    rows = func(DATA_DIR)
    print("Memory use current: Current %d, Peak %d" % tracemalloc.get_traced_memory())
