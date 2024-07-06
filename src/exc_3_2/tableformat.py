
from abc import ABC, abstractmethod
from typing import Sequence, TypeVar, Literal


class ColumnFormatMixin:
    formats = []

    def row(self, rowdata):
        rowdata = [(fmt % d) for fmt, d in zip(self.formats, rowdata)]
        super().row(rowdata)


class UpperHeadersMixin:
    def headings(self, headers: list[str]):
        super().headings([h.upper() for h in headers])


class TableFormatter(ABC):
    @abstractmethod
    def headings(self, headers):
        raise NotImplementedError()

    @abstractmethod
    def row(self, rowdata):
        raise NotImplementedError()


T = TypeVar('T', bound=TableFormatter)


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


def create_formatter(
        format: Literal["text", "csv", "html"],
        column_formats: list[str] | None = None,
        upper_headers: bool = False,
    ) -> T:
    match format:
        case "text":
            formatter_cls = TextTableFormatter
        case "csv":
            formatter_cls = CsvTableFormatter
        case "html":
            formatter_cls = HTMLTableFormatter
        case _:
            raise ValueError("Wrong format selected")

    if column_formats:
        class formatter_cls(ColumnFormatMixin, formatter_cls):
            formats = column_formats

    if upper_headers:
        class formatter_cls(UpperHeadersMixin, formatter_cls):
            pass

    return formatter_cls()


def print_table(data: list[Sequence], attrs: list[str], formatter: T) -> None:
    if not isinstance(formatter, TableFormatter):
        raise TypeError(f"Expected a {TableFormatter}")
    formatter.headings(attrs)
    for record in data:
        row_data = [getattr(record, col) for col in attrs]
        formatter.row(row_data)
