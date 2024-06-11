
from typing import Sequence, Type, Literal


class TableFormatter:
    def headings(self, headers):
        raise NotImplementedError()

    def row(self, rowdata):
        raise NotImplementedError()


T = Type[TableFormatter]


class TextTableFormatter(TableFormatter):
    def headings(self, headers):
        print(" ".join(f"{h:>10}" for h in headers))
        print(("-"*10 + " ")*len(headers))

    def row(self, rowdata):
        print(" ".join(f"{d:>10}" for d in rowdata))


class CsvTableFormatter(TableFormatter):
    def headings(self, headers):
        print(",".join(headers))

    def row(self, rowdata):
        print(",".join(str(v) for v in rowdata))


class HTMLTableFormatter(TableFormatter):
    ROW_OPEN_TAG = "<tr>"
    ROW_CLOSED_TAG = "</tr>"

    def headings(self, headers):
        header_cells = [f"<th>{h}</th>" for h in headers]
        print(" ".join([self.ROW_OPEN_TAG, *header_cells, self.ROW_CLOSED_TAG]))

    def row(self, rowdata):
        row_cells = [f"<td>{str(v)}</td>" for v in rowdata]
        print(" ".join([self.ROW_OPEN_TAG, *row_cells, self.ROW_CLOSED_TAG]))


def create_formatter(format: Literal["text", "csv", "html"]) -> T:
    match format:
        case "text":
            return TextTableFormatter()
        case "csv":
            return CsvTableFormatter()
        case "html":
            return HTMLTableFormatter()
        case _:
            raise ValueError("Wrong format selected")


def print_table(data: list[Sequence], attrs: list[str], formatter: T) -> None:
    formatter.headings(attrs)
    for record in data:
        row_data = [getattr(record, col) for col in attrs]
        formatter.row(row_data)
