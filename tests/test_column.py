import pytest

from queryweaver import Column


@pytest.fixture
def TestColumn():
    return Column("table", "column")


@pytest.fixture
def AnotherTestColumn():
    return Column("table", "anotherColumn")


def test_column_str(TestColumn, AnotherTestColumn):
    assert str(TestColumn) == "table.column"
    assert str(AnotherTestColumn) == "table.anotherColumn"


def test_column_expressions(TestColumn, AnotherTestColumn):
    assert str(TestColumn.count()) == "COUNT(table.column)"
    assert str(TestColumn.sum()) == "SUM(table.column)"
    assert str(TestColumn.min()) == "MIN(table.column)"
    assert str(TestColumn.max()) == "MAX(table.column)"
    assert str(TestColumn.avg()) == "AVG(table.column)"
    assert str(TestColumn.between(1, 10)) == "table.column BETWEEN 1 AND 10"
    assert str(TestColumn.like("*")) == "table.column LIKE '*'"
    assert str(TestColumn.contains((1, 2, 3))) == "table.column IN (1, 2, 3)"


def test_column_arithmetic_alias(TestColumn, AnotherTestColumn):
    test_arithmetic = (TestColumn + AnotherTestColumn).alias("col1 + col2")
    assert str(test_arithmetic) == "(table.column + table.anotherColumn) AS 'col1 + col2'"
    assert test_arithmetic.header == "col1 + col2"
