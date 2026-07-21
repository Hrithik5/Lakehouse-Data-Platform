from pyspark.sql.functions import col, trim, lower, to_timestamp


def transform_orders(df):

    # ---------------- Remove Duplicate Rows ---------------- #

    df = df.dropDuplicates()

    # ---------------- Remove NULL Primary Key ---------------- #

    df = df.filter(col("order_id").isNotNull())

    # ---------------- Validate Primary Key ---------------- #

    duplicate_pk = (
        df.groupBy("order_id")
          .count()
          .filter(col("count") > 1)
    )

    if duplicate_pk.count() > 0:
        raise ValueError("Duplicate order_id found.")

    # ---------------- Remove NULL Foreign Key ---------------- #

    df = df.filter(col("customer_id").isNotNull())

    # ---------------- Standardize Order Status ---------------- #

    df = (
        df.withColumn(
            "order_status",
            lower(trim(col("order_status")))
        )
    )

    # ---------------- Convert Date Columns ---------------- #

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for column in date_columns:
        df = df.withColumn(
            column,
            to_timestamp(col(column))
        )

    return df