from logger import logger
from config import WRITE_GOLD

from load import write_dataset
from gold_registry import GOLD_TABLES

from utils import Timer


def run_gold_pipeline(silver_dataframes):
    """
    Builds all Gold analytical tables.

    Returns
    -------
    dict
        Dictionary containing all Gold DataFrames.
    """

    gold_timer = Timer()

    gold_dataframes = {}

    logger.info("=" * 80)
    logger.info("Starting Gold Layer")
    logger.info("=" * 80)

    for table_name, builder in GOLD_TABLES.items():

        dataset_timer = Timer()

        logger.info(f"Building Gold Dataset : {table_name}")

        # ------------------------------------------------------------------ #
        # Build Gold Dataset
        # ------------------------------------------------------------------ #

        gold_df = builder(silver_dataframes)

        gold_dataframes[table_name] = gold_df

        # Cache only if the DataFrame will be reused
        cache_enabled = WRITE_GOLD

        if cache_enabled:
            gold_df = gold_df.cache()

        row_count = gold_df.count()

        logger.info(
            f"Rows Produced : {row_count:,} | Cached : {'Yes' if cache_enabled else 'No'}"
        )

        # ------------------------------------------------------------------ #
        # Write Gold Layer
        # ------------------------------------------------------------------ #

        if WRITE_GOLD:

            write_timer = Timer()

            output_path = write_dataset(
                gold_df,
                table_name,
                "gold"
            )

            logger.info(
                f"✓ Gold Layer written ({write_timer.elapsed()} sec)"
            )

            logger.info(
                f"Output Path : {output_path}"
            )

            # Release cached memory
            if cache_enabled:
                gold_df.unpersist()

        else:

            logger.info(
                "Gold write skipped (development mode)."
            )

        logger.info(
            f"{table_name} completed in {dataset_timer.elapsed()} sec"
        )

        logger.info("-" * 80)

    logger.info("=" * 80)
    logger.info(
        f"Gold Layer Completed ({gold_timer.elapsed()} sec)"
    )
    logger.info("=" * 80)

    return gold_dataframes