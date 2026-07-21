from logger import logger
from config import WRITE_BRONZE, WRITE_SILVER

from quality import (
    get_dataset_summary,
    get_schema,
    get_null_summary
)

from load import write_dataset
from transformations_registry import TRANSFORMERS
from utils import Timer


# =============================================================================
# Bronze Pipeline
# =============================================================================

def run_bronze_pipeline(table_name, df):
    """
    Bronze Pipeline

    1. Data Quality Validation
    2. Bronze Write

    Returns
    -------
    Spark DataFrame (Cached Raw DataFrame)
    """

    dataset_timer = Timer()

    logger.info("=" * 80)
    logger.info(f"Processing Dataset : {table_name}")
    logger.info("=" * 80)

    try:

        # ------------------------------------------------------------------ #
        # Cache
        # ------------------------------------------------------------------ #

        logger.info("[DEBUG] Step 1 - Cache DataFrame")

        df = df.cache()

        logger.info("[DEBUG] Step 2 - Materialize Cache")

        df.count()

        logger.info("[DEBUG] ✓ Cache Materialized")

        # ------------------------------------------------------------------ #
        # Dataset Summary
        # ------------------------------------------------------------------ #

        logger.info("[DEBUG] Step 3 - Dataset Summary")

        summary = get_dataset_summary(df)

        logger.info(
            f"Rows         : {summary['rows']:,}\n"
            f"Columns      : {summary['columns']}\n"
            f"Null Columns : {summary['null_columns']}"
        )

        # ------------------------------------------------------------------ #
        # Schema
        # ------------------------------------------------------------------ #

        logger.info("[DEBUG] Step 4 - Schema")

        logger.info(f"\nSchema:\n{get_schema(df)}")

        # ------------------------------------------------------------------ #
        # Null Summary
        # ------------------------------------------------------------------ #

        logger.info("[DEBUG] Step 5 - Null Summary")

        null_summary = get_null_summary(df)

        if null_summary:

            logger.info("Null Summary:")

            for column, count in null_summary.items():
                logger.info(f"   • {column}: {count}")

        else:

            logger.info("No null values found.")

        # ------------------------------------------------------------------ #
        # Bronze Write
        # ------------------------------------------------------------------ #

        logger.info("[DEBUG] Step 6 - Bronze Write")

        if WRITE_BRONZE:

            bronze_timer = Timer()

            output_path = write_dataset(
                df,
                table_name,
                "bronze"
            )

            logger.info(
                f"✓ Bronze Layer written ({bronze_timer.elapsed()} sec)"
            )

            logger.info(f"Output Path : {output_path}")

        else:

            logger.info("Bronze write skipped (development mode).")

        logger.info("[DEBUG] ✓ Bronze Write Completed")

        logger.info(
            f"Bronze Completed in {dataset_timer.elapsed()} sec"
        )

        logger.info("=" * 80)

        return df

    except Exception:

        logger.exception(
            f"[DEBUG] Bronze Pipeline Failed : {table_name}"
        )

        raise


# =============================================================================
# Silver Pipeline
# =============================================================================

def run_silver_pipeline(table_name, bronze_df):
    """
    Silver Pipeline

    1. Silver Transformation
    2. Silver Write

    Returns
    -------
    Spark DataFrame (Silver)
    """

    dataset_timer = Timer()

    if table_name in TRANSFORMERS:

        transform_timer = Timer()

        logger.info(
            f"Applying Silver Transformation : {table_name}"
        )

        silver_df = TRANSFORMERS[table_name](bronze_df)

        logger.info(
            f"✓ Transformation completed ({transform_timer.elapsed()} sec)"
        )

        # Bronze DataFrame no longer needed
        bronze_df.unpersist()

        # -------------------------------------------------------------- #
        # Cache Silver
        # -------------------------------------------------------------- #

        silver_df = silver_df.cache()

        # Materialize cache
        row_count = silver_df.count()

        logger.info(
            f"Silver Rows : {row_count:,} | Cached : Yes"
        )

        if WRITE_SILVER:

            silver_timer = Timer()

            output_path = write_dataset(
                silver_df,
                table_name,
                "silver"
            )

            logger.info(
                f"✓ Silver Layer written ({silver_timer.elapsed()} sec)"
            )

            logger.info(f"Output Path : {output_path}")

        else:

            logger.info(
                "Silver write skipped (development mode)."
            )

        logger.info(
            f"Silver Completed in {dataset_timer.elapsed()} sec"
        )

        logger.info("=" * 80)

        return silver_df

    # ------------------------------------------------------------------ #
    # No Transformation
    # ------------------------------------------------------------------ #

    bronze_df.unpersist()

    logger.info(
        "No Silver transformation registered."
    )

    logger.info(
        f"Silver Completed in {dataset_timer.elapsed()} sec"
    )

    logger.info("=" * 80)

    return bronze_df