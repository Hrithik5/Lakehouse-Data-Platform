from confest import spark
from integrity import validate_foreign_key


def test_valid_foreign_keys(spark):
    """
    All child keys exist in parent.
    Should return zero invalid records.
    """

    child = spark.createDataFrame(
        [
            ("C001",),
            ("C002",),
            ("C003",)
        ],
        ["customer_id"]
    )

    parent = spark.createDataFrame(
        [
            ("C001",),
            ("C002",),
            ("C003",)
        ],
        ["customer_id"]
    )

    invalid = validate_foreign_key(
        child,
        parent,
        "customer_id",
        "customer_id"
    )

    assert invalid.count() == 0


def test_invalid_foreign_keys(spark):
    """
    One child key does not exist in parent.
    """

    child = spark.createDataFrame(
        [
            ("C001",),
            ("C002",),
            ("C999",)
        ],
        ["customer_id"]
    )

    parent = spark.createDataFrame(
        [
            ("C001",),
            ("C002",)
        ],
        ["customer_id"]
    )

    invalid = validate_foreign_key(
        child,
        parent,
        "customer_id",
        "customer_id"
    )

    assert invalid.count() == 1

    row = invalid.first()

    assert row.customer_id == "C999"


def test_null_foreign_keys_are_ignored(spark):
    """
    NULL foreign keys should not be reported
    as invalid.
    """

    child = spark.createDataFrame(
        [
            (None,),
            ("C001",)
        ],
        ["customer_id"]
    )

    parent = spark.createDataFrame(
        [
            ("C001",)
        ],
        ["customer_id"]
    )

    invalid = validate_foreign_key(
        child,
        parent,
        "customer_id",
        "customer_id"
    )

    assert invalid.count() == 0


def test_multiple_invalid_foreign_keys(spark):
    """
    Multiple missing parent keys should all
    be returned.
    """

    child = spark.createDataFrame(
        [
            ("C001",),
            ("C999",),
            ("C888",)
        ],
        ["customer_id"]
    )

    parent = spark.createDataFrame(
        [
            ("C001",)
        ],
        ["customer_id"]
    )

    invalid = validate_foreign_key(
        child,
        parent,
        "customer_id",
        "customer_id"
    )

    assert invalid.count() == 2

    invalid_keys = {
        row.customer_id
        for row in invalid.collect()
    }

    assert invalid_keys == {
        "C999",
        "C888"
    }


def test_duplicate_invalid_foreign_keys(spark):
    """
    Duplicate invalid keys should all be returned.
    The function validates rows, not distinct keys.
    """

    child = spark.createDataFrame(
        [
            ("C999",),
            ("C999",),
            ("C001",)
        ],
        ["customer_id"]
    )

    parent = spark.createDataFrame(
        [
            ("C001",)
        ],
        ["customer_id"]
    )

    invalid = validate_foreign_key(
        child,
        parent,
        "customer_id",
        "customer_id"
    )

    assert invalid.count() == 2