from pyspark.sql.functions import col, coalesce, lit, when


def transform_order_payments(df):

    # ---------------- Remove Duplicate Rows ---------------- #

    df = df.dropDuplicates()

    # ---------------- Remove NULL Foreign Key ---------------- #

    df = df.filter(col("order_id").isNotNull())

    # ---------------- Replace NULL Payment Type ---------------- #

    df = df.withColumn(
        "payment_type",
        coalesce(col("payment_type"), lit("Unknown"))
    )

    # ---------------- Validate Payment Value ---------------- #

    df = df.withColumn(
        "payment_value",
        when(col("payment_value") < 0, None)
        .otherwise(col("payment_value"))
    )

    # ---------------- Validate Installments ---------------- #

    df = df.withColumn(
        "payment_installments",
        when(col("payment_installments") < 1, None)
        .otherwise(col("payment_installments"))
    )

    return df