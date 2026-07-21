from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    first,
    countDistinct,
    count,
    sum,
    avg,
    round
)


def build_seller_summary(dataframes: dict) -> DataFrame:

    sellers = dataframes["sellers_dataset"]
    order_items = dataframes["order_items_dataset"]

    # ---------------- Join ---------------- #

    seller_orders = (
        sellers.join(
            order_items,
            on="seller_id",
            how="left"
        )
    )

    # ---------------- Aggregate ---------------- #

    seller_summary = (
        seller_orders
        .groupBy("seller_id")
        .agg(
            first("seller_city").alias("seller_city"),

            first("seller_state").alias("seller_state"),

            countDistinct("order_id").alias("total_orders"),

            count("order_item_id").alias("total_products_sold"),

            sum("price").alias("total_revenue"),

            sum("freight_value").alias("total_freight"),

            avg("price").alias("average_product_price")
        )
    )

    # ---------------- Round Numeric Columns ---------------- #

    seller_summary = (
        seller_summary
        .withColumn(
            "total_revenue",
            round("total_revenue", 2)
        )
        .withColumn(
            "total_freight",
            round("total_freight", 2)
        )
        .withColumn(
            "average_product_price",
            round("average_product_price", 2)
        )
    )

    return seller_summary