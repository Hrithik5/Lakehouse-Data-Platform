from pyspark.sql.functions import col, coalesce, lit, trim

def transform_sellers(df):

    # Remove duplicate rows
    df = df.dropDuplicates()

    # Remove rows with NULL PK
    df = df.filter(col("seller_id").isNotNull())

    # Validate PK uniqueness
    duplicate_pk = (
        df.groupBy("seller_id")
            .count()
            .filter(col("count") > 1)
    )

    if duplicate_pk.count() > 0:
        raise ValueError("Duplicate seller_id found.")

    # Replace NULL city/state
    df = (
        df.withColumn(
            "seller_city",
            coalesce(col("seller_city"), lit("Unknown"))
        )
        .withColumn(
            "seller_state",
            coalesce(col("seller_state"), lit("Unknown"))
        )
    )

    # Trim text columns
    df = (
        df.withColumn(
            "seller_city",
            trim(col("seller_city"))
        )
        .withColumn(
            "seller_state",
            trim(col("seller_state"))
        )
    )

    return df