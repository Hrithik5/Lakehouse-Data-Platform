from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    first,
    sum,
    avg,
    min,
    max,
    countDistinct
)

from gold.payment_summary import build_payment_summary


def build_customer_summary(dataframes: dict) -> DataFrame: 

    customers = dataframes["customers_dataset"]
    orders = dataframes["orders_dataset"]

    payment_summary = build_payment_summary(dataframes)

    customer_orders = (
        customers.join(
            orders,
            on="customer_id",
            how="left"
        )
    )

    customer_orders_payments = (
        customer_orders.join(
            payment_summary,
            on="order_id",
            how="left"
        )
    )

    customer_summary = (
    customer_orders_payments
    .groupBy("customer_id")
    .agg(
        first("customer_city").alias("customer_city"),
        first("customer_state").alias("customer_state"),

        countDistinct("order_id").alias("total_orders"),

        sum("total_payment").alias("total_spent"),

        avg("total_payment").alias("average_order_value"),

        min("order_purchase_timestamp").alias("first_purchase"),

        max("order_purchase_timestamp").alias("last_purchase")
    )
)

    return customer_summary