from confest import spark
import pytest

from pyspark.sql.functions import col

from transformations.products import transform_products


def test_transform_products_success(spark):

    data = [
        (
            "P001",
            " electronics ",
            10,
            100,
            20,
            30,
            40
        )
    ]

    columns = [
        "product_id",
        "product_category_name",
        "product_name_lenght",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_products(df)

    assert result.count() == 1

    row = result.first()

    assert row.product_id == "P001"
    assert row.product_category_name == "electronics"
    assert row.product_weight_g == 100
    assert row.product_length_cm == 20
    assert row.product_height_cm == 30
    assert row.product_width_cm == 40


def test_duplicate_rows_removed(spark):

    data = [
        (
            "P001",
            "electronics",
            10,
            100,
            20,
            30,
            40
        ),
        (
            "P001",
            "electronics",
            10,
            100,
            20,
            30,
            40
        )
    ]

    columns = [
        "product_id",
        "product_category_name",
        "product_name_lenght",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_products(df)

    assert result.count() == 1


def test_null_product_id_removed(spark):

    data = [
        (
            None,
            "electronics",
            10,
            100,
            20,
            30,
            40
        ),
        (
            "P002",
            "books",
            20,
            150,
            15,
            5,
            12
        )
    ]

    columns = [
        "product_id",
        "product_category_name",
        "product_name_lenght",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_products(df)

    assert result.count() == 1
    assert result.first().product_id == "P002"


def test_duplicate_product_id_raises_error(spark):

    data = [
        (
            "P001",
            "electronics",
            10,
            100,
            20,
            30,
            40
        ),
        (
            "P001",
            "books",
            20,
            200,
            15,
            25,
            35
        )
    ]

    columns = [
        "product_id",
        "product_category_name",
        "product_name_lenght",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]

    df = spark.createDataFrame(data, columns)

    with pytest.raises(ValueError):

        transform_products(df)


def test_negative_measurements_become_null(spark):

    data = [
        (
            "P001",
            "electronics",
            10,
            -100,
            -20,
            -30,
            -40
        )
    ]

    columns = [
        "product_id",
        "product_category_name",
        "product_name_lenght",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_products(df)

    row = result.first()

    assert row.product_weight_g is None
    assert row.product_length_cm is None
    assert row.product_height_cm is None
    assert row.product_width_cm is None


def test_trim_product_category(spark):

    data = [
        (
            "P001",
            "   furniture   ",
            10,
            100,
            20,
            30,
            40
        )
    ]

    columns = [
        "product_id",
        "product_category_name",
        "product_name_lenght",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_products(df)

    row = result.first()

    assert row.product_category_name == "furniture"