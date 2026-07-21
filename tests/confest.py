import pytest

from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    """
    Creates a SparkSession for all tests.
    Runs once per testing session.
    """

    spark = (
        SparkSession.builder
        .master("local[*]")
        .appName("PySpark Unit Tests")
        .getOrCreate()
    )

    yield spark

    spark.stop()