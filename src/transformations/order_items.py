from pyspark.sql.functions import col, to_timestamp, when


def transform_order_items(df):

    # ---------------- Remove Duplicate Rows ---------------- #

    df = df.dropDuplicates()

    # ---------------- Remove NULL Composite PK ---------------- #

    df = df.filter(
        col("order_id").isNotNull() &
        col("order_item_id").isNotNull()
    )

    # ---------------- Validate Composite Primary Key ---------------- #

    duplicate_pk = (
        df.groupBy("order_id", "order_item_id")
          .count()
          .filter(col("count") > 1)
    )

    if duplicate_pk.count() > 0:
        raise ValueError("Duplicate composite primary key found.")

    # ---------------- Remove NULL Foreign Keys ---------------- #

    df = df.filter(
        col("product_id").isNotNull() &
        col("seller_id").isNotNull()
    )

    # ---------------- Validate Price ---------------- #

    df = df.withColumn(
        "price",
        when(col("price") < 0, None)
        .otherwise(col("price"))
    )

    # ---------------- Validate Freight ---------------- #

    df = df.withColumn(
        "freight_value",
        when(col("freight_value") < 0, None)
        .otherwise(col("freight_value"))
    )

    # ---------------- Convert Timestamp ---------------- #

    df = df.withColumn(
        "shipping_limit_date",
        to_timestamp(col("shipping_limit_date"))
    )

    return df