from pathlib import Path

from spark import create_spark
from extract import read_csv

from pipeline import (
    run_bronze_pipeline,
    run_silver_pipeline
)

from integrity import validate_foreign_key
from integrity_registry import RELATIONSHIPS

from silver_validation import (
    validate_primary_key,
    PRIMARY_KEYS
)

from gold_pipeline import run_gold_pipeline

from config import (
    STORAGE_BACKEND,
    RUN_REFERENTIAL_INTEGRITY,
    RUN_SILVER_VALIDATION,
    RUN_GOLD
)

from utils import Timer
from logger import logger


# =============================================================================
# Datasets
# =============================================================================

DATASETS = [
    "customers_dataset.csv",
    "geolocation_dataset.csv",
    "order_items_dataset.csv",
    "order_payments_dataset.csv",
    "order_reviews_dataset.csv",
    "orders_dataset.csv",
    "product_category_name_translation.csv",
    "products_dataset.csv",
    "sellers_dataset.csv",
]


# =============================================================================
# ETL Pipeline
# =============================================================================

def run_pipeline():

    spark = create_spark()

    logger.info(f"Storage Backend : {STORAGE_BACKEND.upper()}")

    pipeline_timer = Timer()

    # =========================================================================
    # Extract + Bronze + Silver
    # =========================================================================

    silver_dataframes = {}

    for dataset in DATASETS:

        table_name = Path(dataset).stem

        logger.info("=" * 80)
        logger.info(f"Starting Pipeline : {table_name}")
        logger.info("=" * 80)

        dataset_timer = Timer()

        # ---------------------------------------------------------------------
        # Extract
        # ---------------------------------------------------------------------

        logger.info("Reading Dataset...")

        raw_df = read_csv(
            spark,
            dataset
        )

        logger.info("✓ Extract Completed")

        # ---------------------------------------------------------------------
        # Bronze
        # ---------------------------------------------------------------------

        bronze_df = run_bronze_pipeline(
            table_name,
            raw_df
        )

        # Raw DataFrame reference no longer needed
        del raw_df

        # ---------------------------------------------------------------------
        # Silver
        # ---------------------------------------------------------------------

        silver_df = run_silver_pipeline(
            table_name,
            bronze_df
        )

        silver_dataframes[table_name] = silver_df

        logger.info(
            f"✓ Dataset Pipeline Completed in "
            f"{dataset_timer.elapsed()} sec"
        )

        logger.info("=" * 80)

    # =========================================================================
    # Referential Integrity
    # =========================================================================

    if RUN_REFERENTIAL_INTEGRITY:

        integrity_timer = Timer()

        logger.info("=" * 80)
        logger.info("Starting Referential Integrity Validation")
        logger.info("=" * 80)

        for child_table, parent_table, child_key, parent_key in RELATIONSHIPS:

            invalid_df = validate_foreign_key(
                silver_dataframes[child_table],
                silver_dataframes[parent_table],
                child_key,
                parent_key
            )

            invalid_rows = invalid_df.count()

            invalid_keys = (
                invalid_df
                .select(child_key)
                .distinct()
                .count()
            )

            if invalid_rows == 0:

                logger.info(
                    f"✓ {child_table}.{child_key} -> "
                    f"{parent_table}.{parent_key} PASSED"
                )

            else:

                logger.error(
                    f"✗ {child_table}.{child_key} -> "
                    f"{parent_table}.{parent_key} FAILED"
                )

                logger.error(f"Invalid Rows : {invalid_rows}")
                logger.error(f"Invalid Keys : {invalid_keys}")

                logger.info("Sample Invalid Keys:")

                (
                    invalid_df
                    .select(child_key)
                    .distinct()
                    .show(10, truncate=False)
                )

        logger.info("=" * 80)
        logger.info("Referential Integrity Validation Completed")
        logger.info(
            f"Completed in {integrity_timer.elapsed()} sec"
        )
        logger.info("=" * 80)

    else:

        logger.info(
            "Referential Integrity Validation Skipped."
        )

    # =========================================================================
    # Silver Validation
    # =========================================================================

    if RUN_SILVER_VALIDATION:

        validation_timer = Timer()

        logger.info("=" * 80)
        logger.info("Starting Silver Validation")
        logger.info("=" * 80)

        for table_name, pk_columns in PRIMARY_KEYS.items():

            validate_primary_key(
                silver_dataframes[table_name],
                table_name,
                pk_columns
            )

        logger.info("=" * 80)
        logger.info("Silver Validation Completed")
        logger.info(
            f"Completed in {validation_timer.elapsed()} sec"
        )
        logger.info("=" * 80)

    else:

        logger.info(
            "Silver Validation Skipped."
        )

    # =========================================================================
    # Gold Pipeline
    # =========================================================================

    if RUN_GOLD:

        gold_timer = Timer()

        run_gold_pipeline(
            silver_dataframes
        )

        logger.info(
            f"✓ Gold Completed in {gold_timer.elapsed()} sec"
        )

    else:

        logger.info(
            "Gold Pipeline Skipped."
        )

    # =========================================================================
    # Cleanup
    # =========================================================================

    logger.info("=" * 80)
    logger.info(
        f"✓ Complete ETL Pipeline Finished "
        f"in {pipeline_timer.elapsed()} sec"
    )
    logger.info("=" * 80)

    for df in silver_dataframes.values():
        df.unpersist()

    spark.stop()