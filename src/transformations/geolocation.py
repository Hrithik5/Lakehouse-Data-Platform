from pyspark.sql.functions import col, trim, when


def transform_geolocation(df):

    # ---------------- Remove Duplicate Rows ---------------- #

    df = df.dropDuplicates()

    # ---------------- Trim Text Columns ---------------- #

    df = (
        df.withColumn(
            "geolocation_city",
            trim(col("geolocation_city"))
        )
        .withColumn(
            "geolocation_state",
            trim(col("geolocation_state"))
        )
    )

    # ---------------- Validate Latitude ---------------- #

    df = df.withColumn(
        "geolocation_lat",
        when(
            (col("geolocation_lat") < -90) |
            (col("geolocation_lat") > 90),
            None
        ).otherwise(col("geolocation_lat"))
    )

    # ---------------- Validate Longitude ---------------- #

    df = df.withColumn(
        "geolocation_lng",
        when(
            (col("geolocation_lng") < -180) |
            (col("geolocation_lng") > 180),
            None
        ).otherwise(col("geolocation_lng"))
    )

    return df