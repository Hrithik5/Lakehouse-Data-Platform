from confest import spark
import pytest

from transformations.category_translation import (
    transform_product_category
)


def test_transform_product_category_success(spark):

    data = [
        (
            " electronics ",
            " electronics "
        )
    ]

    columns = [
        "product_category_name",
        "product_category_name_english"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_product_category(df)

    assert result.count() == 1

    row = result.first()

    assert row.product_category_name == "electronics"
    assert row.product_category_name_english == "electronics"


def test_duplicate_rows_removed(spark):

    data = [
        (
            "electronics",
            "electronics"
        ),
        (
            "electronics",
            "electronics"
        )
    ]

    columns = [
        "product_category_name",
        "product_category_name_english"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_product_category(df)

    assert result.count() == 1


def test_null_primary_key_removed(spark):

    data = [
        (
            None,
            "electronics"
        ),
        (
            "books",
            "books"
        )
    ]

    columns = [
        "product_category_name",
        "product_category_name_english"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_product_category(df)

    assert result.count() == 1
    assert result.first().product_category_name == "books"


def test_duplicate_primary_key_raises_error(spark):

    data = [
        (
            "electronics",
            "electronics"
        ),
        (
            "electronics",
            "gadgets"
        )
    ]

    columns = [
        "product_category_name",
        "product_category_name_english"
    ]

    df = spark.createDataFrame(data, columns)

    with pytest.raises(ValueError):

        transform_product_category(df)


def test_trim_text_columns(spark):

    data = [
        (
            "   furniture   ",
            "   furniture   "
        )
    ]

    columns = [
        "product_category_name",
        "product_category_name_english"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_product_category(df)

    row = result.first()

    assert row.product_category_name == "furniture"
    assert row.product_category_name_english == "furniture"