from confest import spark
from pipeline import run_pipeline


def test_pipeline_with_registered_transformation(spark):
    """
    Pipeline should apply the registered transformation
    and return the transformed DataFrame.
    """

    data = [
        (
            "C001",
            "U001",
            "12345",
            " Mumbai ",
            "MH"
        ),
        (
            "C001",
            "U001",
            "12345",
            " Mumbai ",
            "MH"
        )
    ]

    columns = [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state"
    ]

    df = spark.createDataFrame(data, columns)

    result = run_pipeline(
        "customers_dataset",
        df
    )

    # Duplicate should be removed
    assert result.count() == 1

    row = result.first()

    assert row.customer_id == "C001"

    # Trim should occur
    assert row.customer_city == "Mumbai"


def test_pipeline_without_registered_transformation(spark):
    """
    If no transformation exists,
    pipeline should return the original DataFrame.
    """

    data = [
        (
            1,
            "ABC"
        )
    ]

    columns = [
        "id",
        "value"
    ]

    df = spark.createDataFrame(data, columns)

    result = run_pipeline(
        "dummy_table",
        df
    )

    assert result.count() == 1

    row = result.first()

    assert row.id == 1
    assert row.value == "ABC"


def test_pipeline_returns_dataframe(spark):
    """
    Pipeline should always return
    a Spark DataFrame.
    """

    data = [
        (
            "C001",
            "U001",
            "12345",
            "Mumbai",
            "MH"
        )
    ]

    columns = [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state"
    ]

    df = spark.createDataFrame(data, columns)

    result = run_pipeline(
        "customers_dataset",
        df
    )

    assert result is not None

    assert hasattr(result, "count")

    assert hasattr(result, "columns")


def test_pipeline_preserves_schema(spark):
    """
    Transformation should not remove
    required columns.
    """

    data = [
        (
            "C001",
            "U001",
            "12345",
            "Mumbai",
            "MH"
        )
    ]

    columns = [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state"
    ]

    df = spark.createDataFrame(data, columns)

    result = run_pipeline(
        "customers_dataset",
        df
    )

    expected_columns = {
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state"
    }

    assert expected_columns == set(result.columns)