from confest import spark
import pytest

from transformations.sellers import transform_sellers


def test_transform_sellers_success(spark):

    data = [
        (
            "S001",
            " Sao Paulo ",
            " SP "
        )
    ]

    columns = [
        "seller_id",
        "seller_city",
        "seller_state"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_sellers(df)

    assert result.count() == 1

    row = result.first()

    assert row.seller_id == "S001"
    assert row.seller_city == "Sao Paulo"
    assert row.seller_state == "SP"


def test_duplicate_rows_removed(spark):

    data = [
        (
            "S001",
            "Sao Paulo",
            "SP"
        ),
        (
            "S001",
            "Sao Paulo",
            "SP"
        )
    ]

    columns = [
        "seller_id",
        "seller_city",
        "seller_state"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_sellers(df)

    assert result.count() == 1


def test_null_primary_key_removed(spark):

    data = [
        (
            None,
            "Sao Paulo",
            "SP"
        ),
        (
            "S002",
            "Rio",
            "RJ"
        )
    ]

    columns = [
        "seller_id",
        "seller_city",
        "seller_state"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_sellers(df)

    assert result.count() == 1
    assert result.first().seller_id == "S002"


def test_duplicate_primary_key_raises_error(spark):

    data = [
        (
            "S001",
            "Sao Paulo",
            "SP"
        ),
        (
            "S001",
            "Rio",
            "RJ"
        )
    ]

    columns = [
        "seller_id",
        "seller_city",
        "seller_state"
    ]

    df = spark.createDataFrame(data, columns)

    with pytest.raises(ValueError):

        transform_sellers(df)


def test_null_city_state_replaced_with_unknown(spark):

    data = [
        (
            "S001",
            None,
            None
        ),
        (
            "S002",
            "Rio",
            "RJ"
        )
    ]

    columns = [
        "seller_id",
        "seller_city",
        "seller_state"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_sellers(df)

    row = (
        result
        .filter("seller_id = 'S001'")
        .first()
    )

    assert row.seller_city == "Unknown"
    assert row.seller_state == "Unknown"


def test_trim_text_columns(spark):

    data = [
        (
            "S001",
            "   Mumbai   ",
            "   MH   "
        )
    ]

    columns = [
        "seller_id",
        "seller_city",
        "seller_state"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_sellers(df)

    row = result.first()

    assert row.seller_city == "Mumbai"
    assert row.seller_state == "MH"