from pyspark.sql.functions import col, trim, when


def transform_products(df):

    # ---------------- Remove Duplicate Rows ---------------- #

    df = df.dropDuplicates()

    # ---------------- Remove NULL Primary Key ---------------- #

    df = df.filter(col("product_id").isNotNull())

    # ---------------- Validate Primary Key ---------------- #

    duplicate_pk = (
        df.groupBy("product_id")
          .count()
          .filter(col("count") > 1)
    )

    if duplicate_pk.count() > 0:
        raise ValueError("Duplicate product_id found.")

    # ---------------- Trim Text Columns ---------------- #

    df = (
        df.withColumn(
            "product_category_name",
            trim(col("product_category_name"))
        )
    )

    # ---------------- Validate Measurements ---------------- #

    measurement_columns = [
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]

    for column in measurement_columns:
        df = df.withColumn(
            column,
            when(col(column) < 0, None)
            .otherwise(col(column))
        )

    return df