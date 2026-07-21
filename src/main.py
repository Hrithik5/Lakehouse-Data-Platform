from logger import logger
from utils import Timer

from etl_pipeline import run_pipeline


def main():

    logger.info("=" * 80)
    logger.info("Starting ETL Pipeline")

    timer = Timer()

    try:

        run_pipeline()

        logger.info("=" * 80)
        logger.info("ETL Pipeline Completed Successfully")
        logger.info(
            f"Total Execution Time : {timer.elapsed()} sec"
        )
        logger.info("=" * 80)

    except Exception:

        logger.exception("Pipeline Failed")
        raise


if __name__ == "__main__":
    main()