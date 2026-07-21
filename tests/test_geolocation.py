from confest import spark
from pyspark.sql.functions import col

from transformations.geolocation import transform_geolocation


def test_transform_geolocation_success(spark):

    data = [
        (
            "12345",
            -23.5505,
            -46.6333,
            " Sao Paulo ",
            " SP "
        )
    ]

    columns = [
        "geolocation_zip_code_prefix",
        "geolocation_lat",
        "geolocation_lng",
        "geolocation_city",
        "geolocation_state"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_geolocation(df)

    assert result.count() == 1

    row = result.first()

    assert row.geolocation_city == "Sao Paulo"
    assert row.geolocation_state == "SP"
    assert row.geolocation_lat == -23.5505
    assert row.geolocation_lng == -46.6333


def test_duplicate_rows_removed(spark):

    data = [
        (
            "12345",
            -23.5505,
            -46.6333,
            "Sao Paulo",
            "SP"
        ),
        (
            "12345",
            -23.5505,
            -46.6333,
            "Sao Paulo",
            "SP"
        )
    ]

    columns = [
        "geolocation_zip_code_prefix",
        "geolocation_lat",
        "geolocation_lng",
        "geolocation_city",
        "geolocation_state"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_geolocation(df)

    assert result.count() == 1


def test_trim_city_state(spark):

    data = [
        (
            "12345",
            -23.5505,
            -46.6333,
            "   Mumbai   ",
            "   MH   "
        )
    ]

    columns = [
        "geolocation_zip_code_prefix",
        "geolocation_lat",
        "geolocation_lng",
        "geolocation_city",
        "geolocation_state"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_geolocation(df)

    row = result.first()

    assert row.geolocation_city == "Mumbai"
    assert row.geolocation_state == "MH"


def test_invalid_latitude_becomes_null(spark):

    data = [
        (
            "12345",
            120.0,
            -46.6333,
            "Sao Paulo",
            "SP"
        )
    ]

    columns = [
        "geolocation_zip_code_prefix",
        "geolocation_lat",
        "geolocation_lng",
        "geolocation_city",
        "geolocation_state"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_geolocation(df)

    assert result.filter(
        col("geolocation_lat").isNull()
    ).count() == 1


def test_invalid_longitude_becomes_null(spark):

    data = [
        (
            "12345",
            -23.5505,
            -250.0,
            "Sao Paulo",
            "SP"
        )
    ]

    columns = [
        "geolocation_zip_code_prefix",
        "geolocation_lat",
        "geolocation_lng",
        "geolocation_city",
        "geolocation_state"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_geolocation(df)

    assert result.filter(
        col("geolocation_lng").isNull()
    ).count() == 1