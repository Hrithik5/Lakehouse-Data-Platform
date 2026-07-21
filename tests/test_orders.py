import sys
from pathlib import Path
from confest import spark

import pytest
from pyspark.sql.types import TimestampType

# Allow imports from src/
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from transformations.orders import transform_orders


def test_transform_orders(spark):
    """
    Tests the orders transformation.

    Validates:
    - Duplicate rows removed
    - NULL order_id removed
    - NULL customer_id removed
    - order_status standardized
    - Date columns converted to TimestampType
    """

    data = [

        (
            "O001",
            "C001",
            " Delivered ",
            "2018-01-01 10:00:00",
            "2018-01-01 11:00:00",
            "2018-01-02 08:00:00",
            "2018-01-05 16:00:00",
            "2018-01-10 00:00:00"
        ),

        (
            "O001",
            "C001",
            " Delivered ",
            "2018-01-01 10:00:00",
            "2018-01-01 11:00:00",
            "2018-01-02 08:00:00",
            "2018-01-05 16:00:00",
            "2018-01-10 00:00:00"
        ),  # Duplicate row

        (
            None,
            "C002",
            "Shipped",
            "2018-01-03 10:00:00",
            None,
            None,
            None,
            None
        ),  # NULL order_id

        (
            "O003",
            None,
            "Canceled",
            "2018-01-04 10:00:00",
            None,
            None,
            None,
            None
        )  # NULL customer_id

    ]

    columns = [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_orders(df)

    # ------------------------------------------------------ #
    # Row Count
    # ------------------------------------------------------ #

    assert result.count() == 1

    # ------------------------------------------------------ #
    # NULL order_id removed
    # ------------------------------------------------------ #

    assert result.filter("order_id IS NULL").count() == 0

    # ------------------------------------------------------ #
    # NULL customer_id removed
    # ------------------------------------------------------ #

    assert result.filter("customer_id IS NULL").count() == 0

    # ------------------------------------------------------ #
    # Duplicate PK removed
    # ------------------------------------------------------ #

    assert (
        result.select("order_id")
        .distinct()
        .count()
        ==
        result.count()
    )

    # ------------------------------------------------------ #
    # order_status standardized
    # ------------------------------------------------------ #

    order = result.collect()[0]

    assert order.order_status == "delivered"

    # ------------------------------------------------------ #
    # Timestamp conversion
    # ------------------------------------------------------ #

    timestamp_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    schema = result.schema

    for column in timestamp_columns:

        assert isinstance(
            schema[column].dataType,
            TimestampType
        )

def test_duplicate_order_id_raises_error(spark):

    data = [
    (
        "O001",
        "C001",
        "Delivered",
        "2018-01-01 10:00:00",
        "2018-01-01 10:05:00",
        "2018-01-02 10:00:00",
        "2018-01-05 10:00:00",
        "2018-01-10 10:00:00"
    ),

    (
        "O001",
        "C002",
        "Shipped",
        "2018-01-02 10:00:00",
        "2018-01-02 10:05:00",
        "2018-01-03 10:00:00",
        "2018-01-06 10:00:00",
        "2018-01-11 10:00:00"
    )
  ]

    columns = [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    df = spark.createDataFrame(data, columns)

    with pytest.raises(ValueError):

        transform_orders(df)