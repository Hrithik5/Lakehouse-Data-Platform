from pathlib import Path

from config import (
    STORAGE_BACKEND,
    FILE_FORMAT,
    BRONZE_DATA,
    SILVER_DATA,
    GOLD_DATA,
)

from athena_catalog import (
    create_database,
    register_delta_table,
)

LAYER_PATHS = {
    "bronze": BRONZE_DATA,
    "silver": SILVER_DATA,
    "gold": GOLD_DATA,
}


def write_dataset(df, table_name, layer):
    """
    Writes a Spark DataFrame to the specified data layer.

    Parameters
    ----------
    df : pyspark.sql.DataFrame
        DataFrame to write.

    table_name : str
        Name of the table.

    layer : str
        bronze | silver | gold

    Returns
    -------
    str
        Output path.
    """

    if layer not in LAYER_PATHS:
        raise ValueError(
            f"Invalid layer '{layer}'. "
            f"Choose from {list(LAYER_PATHS.keys())}."
        )

    output_path = f"{LAYER_PATHS[layer]}/{table_name}"

    # ------------------------------------------------------------------ #
    # Create local directories only
    # ------------------------------------------------------------------ #

    if STORAGE_BACKEND == "local":
        Path(output_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

    # ------------------------------------------------------------------ #
    # Configure Writer
    # ------------------------------------------------------------------ #

    writer = (
        df.coalesce(1)
        .write
        .mode("overwrite")
    )

    # ------------------------------------------------------------------ #
    # Write Dataset
    # ------------------------------------------------------------------ #

    if FILE_FORMAT == "delta":

        writer.format("delta").save(output_path)

        # -------------------------------------------------------------- #
        # Register Silver/Gold Delta tables in Athena
        # -------------------------------------------------------------- #

        if layer == "gold":

            create_database()

            register_delta_table(
                table_name=table_name,
                s3_location=output_path
            )

    elif FILE_FORMAT == "parquet":

        writer.parquet(output_path)

    else:

        raise ValueError(
            f"Unsupported FILE_FORMAT: {FILE_FORMAT}"
        )

    return output_path