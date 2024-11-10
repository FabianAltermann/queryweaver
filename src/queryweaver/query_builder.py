__all__ = ["SQLQueryBuilder"]

import logging
import sqlite3
from pathlib import Path
from typing import Any

import pandas as pd  # type: ignore

from .tables import Column, Schematic, Table

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SQLQueryBuilder:
    def __init__(
        self, db_path: str, schema: Schematic | None = None, dialect: str = "sqlite"
    ) -> None:
        self.db_path: str = db_path
        self.conn: sqlite3.Connection | None = None
        self.cursor: sqlite3.Cursor | None = None
        self.query: str = ""
        self.values: list[Any] = []
        self.schema: Schematic = schema if schema else Schematic()

    def _connect(self) -> None:
        if not Path(self.db_path).exists():
            raise FileNotFoundError(f"Database file not found at {self.db_path}")
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        if not self.schema.tables:
            self._generate_table_classes()

    def _generate_table_classes(self) -> None:
        assert self.cursor is not None, "Cursor is not initialized."
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names: list[str] = [row[0] for row in self.cursor.fetchall()]

        for table_name in table_names:
            table = Table(table_name)
            self.cursor.execute(f"PRAGMA table_info({table_name});")
            columns: list[str] = [row[1] for row in self.cursor.fetchall()]
            for column_name in columns:
                table.add_column(column_name)
            self.schema.add_table(table_name, table)

    def _add_to_query_string(self, s: str) -> None:
        self.query += f"{s}\n"

    def close(self) -> None:
        if self.conn:
            self.conn.close()

    def __enter__(self) -> "SQLQueryBuilder":
        self._connect()
        return self

    def __exit__(
        self,
        exc_type: type | None,
        exc_value: Exception | None,
        traceback: Any | None,
    ) -> None:
        self.close()

    def __str__(self) -> str:
        return self.query

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(db={self.db_path}, query='{self.query}')"

    def insert_into(self, table: Table, **values: Any) -> "SQLQueryBuilder":
        columns: str = ", ".join(values.keys())
        placeholders: str = ", ".join("?" * len(values))
        self._add_to_query_string(
            f"INSERT INTO {table.table_name} ({columns}) VALUES ({placeholders})"
        )
        self.values = list(values.values())
        return self

    def update(self, table: Table) -> "SQLQueryBuilder":
        self._add_to_query_string(f"UPDATE {table.table_name}")
        return self

    def set(self, **values: Any) -> "SQLQueryBuilder":
        set_clause: str = ", ".join(f"{col} = ?" for col in values)
        self._add_to_query_string(f" SET {set_clause}")
        self.values.extend(values.values())
        return self

    def delete_from(self, table: Table) -> "SQLQueryBuilder":
        self._add_to_query_string(f"DELETE FROM {table.table_name}")
        return self

    def select(self, *columns: Column, distinct: bool = False) -> "SQLQueryBuilder":
        self._add_to_query_string(
            f"SELECT{' DISTINCT ' if distinct else ' '}\n\t"
            + ",\n\t".join(str(col) for col in columns)
        )
        self.selected_columns = [col for col in columns]
        return self

    def from_table(self, table: Table) -> "SQLQueryBuilder":
        self._add_to_query_string(f" FROM {table.table_name}")
        return self

    def where(self, condition: Column, *params: Any | list[Any]) -> "SQLQueryBuilder":
        self._add_to_query_string(f" WHERE {condition}")
        return self

    def having(self, condition: Column) -> "SQLQueryBuilder":
        self._add_to_query_string(f" HAVING {condition}")
        return self

    def join(
        self, table: Table, on: Column, *params: Any, join_type: str = "INNER"
    ) -> "SQLQueryBuilder":
        self._add_to_query_string(f" {join_type.upper()} JOIN {table.table_name} \n\t ON {on}")
        self.values.extend(params)
        return self

    def order_by(self, *columns: Column, ascending: bool = True) -> "SQLQueryBuilder":
        order_clause = ", ".join(str(col) for col in columns)
        direction = "ASC" if ascending else "DESC"
        self._add_to_query_string(f" ORDER BY {order_clause} {direction}")
        return self

    def group_by(self, *columns: Column) -> "SQLQueryBuilder":
        group_clause = ", ".join(str(col) for col in columns)
        self._add_to_query_string(f" GROUP BY {group_clause}")
        return self

    def limit(self, limit: int):
        self._add_to_query_string(f" LIMIT {limit}")
        return self

    def offset(self, offset: int):
        self._add_to_query_string(f" OFFSET {offset}")
        return self

    def execute(self) -> tuple[list[str], list[tuple[Any]]]:
        if not self.conn or not self.cursor:
            raise ConnectionError("Database connection is not established.")
        logger.debug(f"Executing query:\n{self.query}")
        self.cursor.execute(self.query, self.values)
        self.conn.commit()
        result: list[tuple[Any]] = self.cursor.fetchall()
        column_names = list(map(lambda x: x.header, self.selected_columns))
        self.query = ""
        self.values = []
        self.selected_columns = []
        return column_names, result

    def to_pandas(self, **kwargs):
        header, data = self.execute()
        return pd.DataFrame(data, columns=header, **kwargs)
