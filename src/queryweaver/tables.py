__all__ = ["Column", "Table", "Schematic"]

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml  # type: ignore


@dataclass
class Column:
    table_name: str
    column_name: str
    expression: str | None = None
    alias_name: str | None = None

    @property
    def name(self) -> str:
        return f"{self.table_name}.{self.column_name}"

    @property
    def header(self) -> str:
        return self.alias_name or self.name

    def __str__(self) -> str:
        match self.alias_name, self.expression:
            case (None, None):
                return self.name
            case (_, None):
                return f"{self.name} AS '{self.alias_name}'"
            case (None, _):
                #  TODO: Fix this type error
                return self.expression  # type: ignore
            case (_, _):
                return f"{self.expression} AS '{self.alias_name}'"
        return ""

        # if self.alias_name and self.expression:
        #     return f"{self.expression} AS '{self.alias_name}'"
        # elif self.alias_name:
        #     return f"{self.name} AS '{self.alias_name}'"
        # elif self.expression:
        #     return self.expression
        # else:
        #     return f"{self.name}"

    def alias(self, alias_name: str) -> "Column":
        return Column(self.table_name, self.column_name, self.expression, alias_name)

    def contains(self, other: tuple):
        if not isinstance(other, tuple):
            raise NotImplementedError(f"Not Implemented with type {type(other)} - use tuple for IN")
        return f"{self!s} IN {other!s}"

    def between(self, lower: Any, upper: Any):
        return Column(
            self.table_name,
            self.column_name,
            expression=f"{self!s} BETWEEN {lower} AND {upper}",
        )

    def like(self, condition: str):
        return Column(
            self.table_name,
            self.column_name,
            expression=f"{self!s} LIKE '{condition}'",
        )

    def count(self):
        return Column(
            self.table_name,
            self.column_name,
            expression=f"COUNT({self!s})",
        )

    def sum(self):
        return Column(
            self.table_name,
            self.column_name,
            expression=f"SUM({self!s})",
        )

    def min(self):
        return Column(
            self.table_name,
            self.column_name,
            expression=f"MIN({self!s})",
        )

    def max(self):
        return Column(
            self.table_name,
            self.column_name,
            expression=f"MAX({self!s})",
        )

    def avg(self):
        return Column(
            self.table_name,
            self.column_name,
            expression=f"AVG({self!s})",
        )

    def _combine(self, other: Any, operator: str) -> "Column":
        # Combine two columns with the given operator
        return Column(
            self.table_name,
            self.column_name,
            expression=f"({self!s} {operator} {other!s})",
            alias_name=self.alias_name,
        )

    def __add__(self, other):
        return self._combine(other, "+")

    def __sub__(self, other):
        return self._combine(other, "-")

    def __mul__(self, other):
        return self._combine(other, "*")

    def __truediv__(self, other):
        return self._combine(other, "/")

    def __floordiv__(self, other):
        return self._combine(other, "//")

    def __mod__(self, other):
        return self._combine(other, "%")

    def __pow__(self, other):
        return self._combine(other, "**")

    def __eq__(self, other):
        return self._combine(other, "=")

    def __lt__(self, other):
        return self._combine(other, "<")

    def __le__(self, other):
        return self._combine(other, "<=")

    def __gt__(self, other):
        return self._combine(other, ">")

    def __ge__(self, other):
        return self._combine(other, ">=")

    def __hash__(self):
        return hash(str(self))


@dataclass
class Table:
    table_name: str
    columns: dict[str, Column] = field(init=False)

    def __post_init__(self) -> None:
        self.columns = {}

    def add_column(self, column_name: str) -> None:
        column = Column(self.table_name, column_name)
        self.columns[column_name] = column
        setattr(self, column_name, column)

    @property
    def all_columns(self) -> str:
        return ", ".join(str(column) for column in self.columns.values())


@dataclass
class Schematic:
    tables: dict[str, Table] = field(default_factory=dict)

    @staticmethod
    def from_yaml(file_path: str) -> "Schematic":
        with open(Path(file_path).resolve()) as file:
            schema_data = yaml.safe_load(file)

        schema = Schematic()
        for table_name, columns in schema_data.items():
            table = Table(table_name)
            for column_name in columns:
                table.add_column(column_name)
            schema.add_table(table_name, table)

        return schema

    def add_table(self, table_name: str, table: Table) -> None:
        self.tables[table_name] = table
        setattr(self, table_name, table)


if __name__ == "__main__":
    col1 = Column("table", "column1")
    col2 = Column("table", "column2")
    print((col1 + col2).alias("col1 + col2"))
