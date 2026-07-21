from confest import spark
from quality import (
    get_null_summary,
    get_row_count,
    get_column_count,
    get_schema,
    get_dataset_summary
)


def test_get_row_count(spark):

    data = [
        ("A", 1),
        ("B", 2),
        ("C", 3)
    ]

    columns = [
        "name",
        "value"
    ]

    df = spark.createDataFrame(data, columns)

    assert get_row_count(df) == 3


def test_get_column_count(spark):

    data = [
        ("A", 1),
        ("B", 2)
    ]

    columns = [
        "name",
        "value"
    ]

    df = spark.createDataFrame(data, columns)

    assert get_column_count(df) == 2


def test_get_null_summary(spark):

    data = [
        ("A", 1),
        (None, 2),
        ("C", None)
    ]

    columns = [
        "name",
        "value"
    ]

    df = spark.createDataFrame(data, columns)

    result = get_null_summary(df)

    assert result["name"] == 1
    assert result["value"] == 1


def test_get_null_summary_no_nulls(spark):

    data = [
        ("A", 1),
        ("B", 2)
    ]

    columns = [
        "name",
        "value"
    ]

    df = spark.createDataFrame(data, columns)

    result = get_null_summary(df)

    assert result == {}


def test_get_schema(spark):

    data = [
        ("A", 1)
    ]

    columns = [
        "name",
        "value"
    ]

    df = spark.createDataFrame(data, columns)

    schema = get_schema(df)

    assert "name" in schema
    assert "value" in schema
    assert "string" in schema.lower()
    assert "long" in schema.lower()


def test_get_dataset_summary(spark):

    data = [
        ("A", 1),
        (None, 2),
        ("C", None)
    ]

    columns = [
        "name",
        "value"
    ]

    df = spark.createDataFrame(data, columns)

    summary = get_dataset_summary(df)

    assert summary["rows"] == 3
    assert summary["columns"] == 2
    assert summary["null_columns"] == 2


def test_get_dataset_summary_without_nulls(spark):

    data = [
        ("A", 1),
        ("B", 2)
    ]

    columns = [
        "name",
        "value"
    ]

    df = spark.createDataFrame(data, columns)

    summary = get_dataset_summary(df)

    assert summary["rows"] == 2
    assert summary["columns"] == 2
    assert summary["null_columns"] == 0