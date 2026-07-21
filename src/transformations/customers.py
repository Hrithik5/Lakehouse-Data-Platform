from pyspark.sql.functions import col, coalesce, lit, trim

def transform_customers(df):

    # Remove duplicate rows
    df = df.dropDuplicates()

    # Remove rows with NULL PK
    df = df.filter(col("customer_id").isNotNull())

    # Validate PK uniqueness
    duplicate_pk = (
        df.groupBy("customer_id")
            .count()
            .filter(col("count") > 1)
    )

    if duplicate_pk.count() > 0:
        raise ValueError("Duplicate customer_id found.")

    # Replace NULL city/state
    df = (
        df.withColumn(
            "customer_city",
            coalesce(col("customer_city"), lit("Unknown"))
        )
        .withColumn(
            "customer_state",
            coalesce(col("customer_state"), lit("Unknown"))
        )
    )

    # Trim text columns
    df = (
        df.withColumn(
            "customer_city",
            trim(col("customer_city"))
        )
        .withColumn(
            "customer_state",
            trim(col("customer_state"))
        )
    )

    return df