from pyspark.sql.functions import col, coalesce, lit, trim

def transform_product_category(df):

    # Remove duplicate rows
    df = df.dropDuplicates()

    # Remove rows with NULL PK
    df = df.filter(col("product_category_name").isNotNull())

    # Validate PK uniqueness
    duplicate_pk = (
        df.groupBy("product_category_name")
            .count()
            .filter(col("count") > 1)
    )

    if duplicate_pk.count() > 0:
        raise ValueError("Duplicate product_category_name found.")

    # Trim text columns
    df = (
        df.withColumn(
            "product_category_name",
            trim(col("product_category_name"))
        )
        .withColumn(
            "product_category_name_english",
            trim(col("product_category_name_english"))
        )
    )
    return df