from pyspark.sql.functions import col, count, when


def get_null_summary(df):
    """
    Returns a dictionary containing only the
    columns having NULL values.
    """

    null_counts = (
        df.select(
            [
                count(
                    when(col(column).isNull(), column)
                ).alias(column)
                for column in df.columns
            ]
        )
        .first()
        .asDict()
    )

    return {
        column: null_count
        for column, null_count in null_counts.items()
        if null_count > 0
    }


def get_schema(df):
    """
    Returns the Spark schema as a formatted string.
    """

    return df._jdf.schema().treeString()


def get_dataset_summary(df):
    """
    Returns a summary of the dataset.

    NOTE:
    Assumes the DataFrame is already cached by the caller.
    """

    row_count = df.count()

    null_summary = get_null_summary(df)

    return {
        "rows": row_count,
        "columns": len(df.columns),
        "null_columns": len(null_summary),
    }