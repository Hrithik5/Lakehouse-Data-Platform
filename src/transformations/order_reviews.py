from pyspark.sql.functions import col, to_timestamp


def transform_order_reviews(df):

    # Remove duplicate rows
    df = df.dropDuplicates()

    # Remove NULL order_id
    df = df.filter(col("order_id").isNotNull())

    # Keep NULL review comments (optional)

    # ---------------- Convert Date Columns ---------------- #

    date_columns = [
        "review_creation_date",
        "review_answer_timestamp"
    ]

    for column in date_columns:
        df = df.withColumn(
            column,
            to_timestamp(col(column))
        )

    return df