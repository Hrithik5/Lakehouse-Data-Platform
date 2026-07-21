import sys
from pathlib import Path
from confest import spark

import pytest

# Allow importing from src/
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from transformations.customers import transform_customers


def test_transform_customers(spark):
    """
    Tests the customer transformation.

    Validates:
    - Duplicate rows are removed
    - NULL customer_id rows are removed
    - customer_city NULLs become 'Unknown'
    - customer_state NULLs become 'Unknown'
    """

    data = [
        (
            "C001",
            "U001",
            "12345",
            " Sao Paulo ",
            "SP"
        ),

        (
            "C001",
            "U001",
            "12345",
            " Sao Paulo ",
            "SP"
        ),  # Duplicate

        (
            None,
            "U002",
            "22222",
            "Rio",
            "RJ"
        ),  # NULL customer_id

        (
            "C003",
            "U003",
            "33333",
            None,
            None
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

    result = transform_customers(df)

    # ------------------------------------------------------------------ #
    # Row Count
    # ------------------------------------------------------------------ #

    assert result.count() == 2

    # ------------------------------------------------------------------ #
    # No NULL customer_id
    # ------------------------------------------------------------------ #

    assert (
        result
        .filter("customer_id IS NULL")
        .count()
        == 0
    )

    # ------------------------------------------------------------------ #
    # Duplicate PK removed
    # ------------------------------------------------------------------ #

    assert (
        result
        .select("customer_id")
        .distinct()
        .count()
        ==
        result.count()
    )

    # ------------------------------------------------------------------ #
    # Unknown replacement
    # ------------------------------------------------------------------ #

    unknown = (
        result
        .filter("customer_id = 'C003'")
        .collect()[0]
    )

    assert unknown.customer_city == "Unknown"
    assert unknown.customer_state == "Unknown"

    # ------------------------------------------------------------------ #
    # Trim validation
    # ------------------------------------------------------------------ #

    customer = (
        result
        .filter("customer_id = 'C001'")
        .collect()[0]
    )

    assert customer.customer_city == "Sao Paulo"