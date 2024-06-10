import collections
import csv


class DataCollection(collections.abc.Sequence):
    def __init__(self, columns: list[str]) -> None:
        self.columns = {col_name: list() for col_name in columns}

    def __len__(self):
        return len(list(self.columns.values())[0])

    def __getitem__(self, index) -> dict:
        data = {col: values[index] for col, values in self.columns.items()}
        if len(list(data.values())[0]) == 1:
            return data
        else:
            header = self.columns.keys()
            records = []
            values = zip(*data.values())
            for i in values:
                record = {name: val for name, val in zip(header, i)}
                records.append(record)
            return records
    
    def append(self, values: dict):
        for key, value in values.items():
            self.columns[key].append(value)


def read_csv_as_dicts(filepath: str, column_types: list) -> list[dict]:
    records = []
    with open(filepath) as f:
        csv_file = csv.reader(f)
        header = next(csv_file)
        for row in csv_file:
            record = {
                name: func(val) for name, func, val in zip(
                    header, column_types, row
                )
            }
            records.append(record)
    return records


def read_csv_as_columns(filepath: str, column_types: list) -> DataCollection:

    with open(filepath) as f:
        csv_file = csv.reader(f)
        header = next(csv_file)

        data_collection = DataCollection(header)

        for row in csv_file:
            record = {
                name: func(val) for name, func, val in zip(
                    header, column_types, row
                )
            }
            data_collection.append(record)

    return data_collection


def read_csv_as_instances(filename: str, cls: object) -> list[object]:
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        next(rows)
        for row in rows:
            records.append(cls.from_row(row))
    return records


if __name__ == "__main__":
    from pathlib import Path
    path = Path(__file__).parent.parent.parent
    data = read_csv_as_columns(path /"Data/ctabus.csv", [str, str, str, int])
    len(data)
    data[0]
    data[0:3]
