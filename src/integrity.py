from pyspark.sql.functions import col


def validate_foreign_key(
    child_df,
    parent_df,
    child_key,
    parent_key
):
    """
    Returns child records whose foreign key
    does not exist in the parent table.
    """

    child = child_df.alias("child")
    parent = parent_df.alias("parent")

    invalid_df = (
        child
        .filter(col(f"child.{child_key}").isNotNull())
        .join(
            parent,
            col(f"child.{child_key}") == col(f"parent.{parent_key}"),
            "left_anti"
        )
        .select("child.*")
    )

    return invalid_df