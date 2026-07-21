from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    first,
    countDistinct,
    count,
    sum,
    avg,
    round
)


def build_product_summary(dataframes: dict) -> DataFrame:

    products = dataframes["products_dataset"]
    order_items = dataframes["order_items_dataset"]
    reviews = dataframes["order_reviews_dataset"]

    # ---------------- Products + Order Items ---------------- #

    product_orders = (
        products.join(
            order_items,
            on="product_id",
            how="left"
        )
    )

    # ---------------- Join Reviews ---------------- #

    product_reviews = (
        product_orders.join(
            reviews,
            on="order_id",
            how="left"
        )
    )

    # ---------------- Aggregate ---------------- #

    product_summary = (
        product_reviews
        .groupBy("product_id")
        .agg(

            first("product_category_name").alias(
                "product_category_name"
            ),

            countDistinct("order_id").alias(
                "total_orders"
            ),

            count("order_item_id").alias(
                "total_units_sold"
            ),

            sum("price").alias(
                "total_revenue"
            ),

            avg("price").alias(
                "average_price"
            ),

            avg("review_score").alias(
                "average_review_score"
            ),

            count("review_id").alias(
                "total_reviews"
            ),

            countDistinct("seller_id").alias(
                "unique_sellers"
            )

        )
    )

    # ---------------- Round Numeric Columns ---------------- #

    product_summary = (
        product_summary
        .withColumn(
            "total_revenue",
            round("total_revenue", 2)
        )
        .withColumn(
            "average_price",
            round("average_price", 2)
        )
        .withColumn(
            "average_review_score",
            round("average_review_score", 2)
        )
    )

    return product_summary