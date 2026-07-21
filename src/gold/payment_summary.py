from pyspark.sql import DataFrame
from pyspark.sql.functions import sum, first


def build_payment_summary(dataframes: dict) -> DataFrame:

    payments = dataframes["order_payments_dataset"]

    payment_summary = (
        payments
        .groupBy("order_id")
        .agg(
            sum("payment_value").alias("total_payment"),
            first("payment_type").alias("payment_type")
        )
    )

    return payment_summary