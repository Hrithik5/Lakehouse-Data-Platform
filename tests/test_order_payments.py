import pytest
from confest import spark
from pyspark.sql.functions import col

from transformations.order_payments import transform_order_payments


def test_transform_order_payments_success(spark):

    data = [
        (
            "O001",
            1,
            "credit_card",
            2,
            150.75
        )
    ]

    columns = [
        "order_id",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_order_payments(df)

    assert result.count() == 1

    row = result.first()

    assert row.order_id == "O001"
    assert row.payment_type == "credit_card"
    assert row.payment_installments == 2
    assert row.payment_value == 150.75


def test_null_order_id_removed(spark):

    data = [
        (
            None,
            1,
            "credit_card",
            2,
            150.75
        ),
        (
            "O002",
            1,
            "boleto",
            1,
            200.00
        )
    ]

    columns = [
        "order_id",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_order_payments(df)

    assert result.count() == 1
    assert result.first().order_id == "O002"


def test_null_payment_type_becomes_unknown(spark):

    data = [
        (
            "O001",
            1,
            None,
            2,
            150.75
        ),
        (
            "O002",
            1,
            "credit_card",
            1,
            200.00
        )
    ]

    columns = [
        "order_id",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_order_payments(df)

    row = (
        result
        .filter(col("order_id") == "O001")
        .first()
    )

    assert row.payment_type == "Unknown"


def test_negative_payment_value_becomes_null(spark):

    data = [
        (
            "O001",
            1,
            "credit_card",
            2,
            -100.00
        )
    ]

    columns = [
        "order_id",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_order_payments(df)

    assert result.filter(col("payment_value").isNull()).count() == 1


def test_invalid_installments_becomes_null(spark):

    data = [
        (
            "O001",
            1,
            "credit_card",
            0,
            100.00
        )
    ]

    columns = [
        "order_id",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_order_payments(df)

    assert result.filter(
        col("payment_installments").isNull()
    ).count() == 1


def test_duplicate_rows_removed(spark):

    data = [
        (
            "O001",
            1,
            "credit_card",
            2,
            100.00
        ),
        (
            "O001",
            1,
            "credit_card",
            2,
            100.00
        )
    ]

    columns = [
        "order_id",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_order_payments(df)

    assert result.count() == 1