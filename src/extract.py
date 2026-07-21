from config import (
    RAW_DATA,
    FILE_FORMAT,
)
from schema_registry import SCHEMA_REGISTRY

def read_dataset(spark, filename):
    """
    Reads a dataset based on the configured file format.

    Parameters
    ----------
    spark : SparkSession

    filename : str
        CSV filename (for raw)
        or table name (for Bronze/Silver/Gold)

    Returns
    -------
    pyspark.sql.DataFrame
    """

    path = f"{RAW_DATA}/{filename}"

    # --------------------------------------------------------------- #
    # CSV
    # --------------------------------------------------------------- #

    if FILE_FORMAT == "csv":

        return (
            spark.read
            .option("header", True)
            .option("inferSchema", True)
            .option("multiLine", True)
            .option("escape", '"')
            .csv(path)
        )

    # --------------------------------------------------------------- #
    # Parquet
    # --------------------------------------------------------------- #

    elif FILE_FORMAT == "parquet":

        return spark.read.parquet(path)

    # --------------------------------------------------------------- #
    # Delta
    # --------------------------------------------------------------- #

    elif FILE_FORMAT == "delta":

        return (
            spark.read
            .format("delta")
            .load(path)
        )

    else:

        raise ValueError(
            f"Unsupported FILE_FORMAT: {FILE_FORMAT}"
        )


# ------------------------------------------------------------------ #
# Convenience wrapper for raw CSV ingestion
# ------------------------------------------------------------------ #

def read_csv(spark, filename):
    """
    Reads raw CSV files from the landing zone.

    If a schema exists in the schema registry, it is used.
    Otherwise Spark falls back to schema inference.
    """

    path = f"{RAW_DATA}/{filename}"

    reader = (
        spark.read
        .option("header", True)
        .option("multiLine", True)
        .option("escape", '"')
    )

    schema = SCHEMA_REGISTRY.get(filename)

    if schema is not None:

        return (
            reader
            .schema(schema)
            .csv(path)
        )

    return (
        reader
        .option("inferSchema", True)
        .csv(path)
    )