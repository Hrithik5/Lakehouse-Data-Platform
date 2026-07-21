import time

import boto3

from logger import logger
from config import (
    AWS_REGION,
    ATHENA_DATABASE,
    ATHENA_OUTPUT_LOCATION,
)


athena = boto3.client(
    "athena",
    region_name=AWS_REGION
)


def run_query(query: str):
    """
    Execute an Athena query and wait for completion.
    """

    response = athena.start_query_execution(
        QueryString=query,
        ResultConfiguration={
            "OutputLocation": ATHENA_OUTPUT_LOCATION
        }
    )

    execution_id = response["QueryExecutionId"]

    while True:

        result = athena.get_query_execution(
            QueryExecutionId=execution_id
        )

        state = (
            result["QueryExecution"]["Status"]["State"]
        )

        if state == "SUCCEEDED":
            logger.info("Athena query completed.")
            return

        if state in ["FAILED", "CANCELLED"]:

            reason = (
                result["QueryExecution"]["Status"]
                .get("StateChangeReason", "")
            )

            raise RuntimeError(
                f"Athena query failed.\n{reason}"
            )

        time.sleep(2)


def create_database():
    """
    Create Athena database if it does not exist.
    """

    query = f"""
    CREATE DATABASE IF NOT EXISTS {ATHENA_DATABASE}
    """

    logger.info(
        f"Ensuring Athena database '{ATHENA_DATABASE}' exists."
    )

    run_query(query)


def register_delta_table(table_name: str, s3_location: str):

    # Spark uses s3a://
    # Athena requires s3://
    s3_location = s3_location.replace("s3a://", "s3://", 1)

    query = f"""
    CREATE EXTERNAL TABLE IF NOT EXISTS
    {ATHENA_DATABASE}.{table_name}

    LOCATION '{s3_location}'

    TBLPROPERTIES (
        'table_type'='DELTA'
    )
    """

    logger.info(
        f"Registering Delta table '{table_name}'..."
    )

    run_query(query)

    logger.info(
        f"Delta table '{table_name}' registered."
    )