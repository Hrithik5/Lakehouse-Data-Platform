from confest import spark
import pytest

from pyspark.sql.functions import col

from transformations.order_items import transform_order_items


def test_transform_order_items_success(spark):

    data = [
        (
            "O001",
            1,
            "P001",
            "S001",
            "2018-01-01 10:00:00",
            100.0,
            20.0
        )
    ]

    columns = [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_date",
        "price",
        "freight_value"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_order_items(df)

    assert result.count() == 1

    row = result.first()

    assert row.order_id == "O001"
    assert row.order_item_id == 1
    assert row.price == 100.0
    assert row.freight_value == 20.0


def test_duplicate_composite_pk_raises_error(spark):

    data = [
        (
            "O001",
            1,
            "P001",
            "S001",
            "2018-01-01 10:00:00",
            100.0,
            20.0
        ),
        (
            "O001",
            1,
            "P002",
            "S002",
            "2018-01-01 10:00:00",
            150.0,
            30.0
        )
    ]

    columns = [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_date",
        "price",
        "freight_value"
    ]

    df = spark.createDataFrame(data, columns)

    with pytest.raises(ValueError):
        transform_order_items(df)


def test_negative_price_becomes_null(spark):

    data = [
        (
            "O001",
            1,
            "P001",
            "S001",
            "2018-01-01 10:00:00",
            -100.0,
            20.0
        )
    ]

    columns = [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_date",
        "price",
        "freight_value"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_order_items(df)

    assert result.filter(col("price").isNull()).count() == 1


def test_negative_freight_becomes_null(spark):

    data = [
        (
            "O001",
            1,
            "P001",
            "S001",
            "2018-01-01 10:00:00",
            100.0,
            -20.0
        )
    ]

    columns = [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_date",
        "price",
        "freight_value"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_order_items(df)

    assert result.filter(col("freight_value").isNull()).count() == 1