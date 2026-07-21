from confest import spark
from pyspark.sql.types import TimestampType

from transformations.order_reviews import transform_order_reviews


def test_transform_order_reviews_success(spark):

    data = [
        (
            "R001",
            "O001",
            5,
            "Excellent",
            "Very good product",
            "2018-01-01 10:00:00",
            "2018-01-02 11:00:00"
        )
    ]

    columns = [
        "review_id",
        "order_id",
        "review_score",
        "review_comment_title",
        "review_comment_message",
        "review_creation_date",
        "review_answer_timestamp"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_order_reviews(df)

    assert result.count() == 1

    row = result.first()

    assert row.review_id == "R001"
    assert row.order_id == "O001"
    assert row.review_score == 5


def test_duplicate_rows_removed(spark):

    data = [
        (
            "R001",
            "O001",
            5,
            "Excellent",
            "Very good product",
            "2018-01-01 10:00:00",
            "2018-01-02 11:00:00"
        ),
        (
            "R001",
            "O001",
            5,
            "Excellent",
            "Very good product",
            "2018-01-01 10:00:00",
            "2018-01-02 11:00:00"
        )
    ]

    columns = [
        "review_id",
        "order_id",
        "review_score",
        "review_comment_title",
        "review_comment_message",
        "review_creation_date",
        "review_answer_timestamp"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_order_reviews(df)

    assert result.count() == 1


def test_null_order_id_removed(spark):

    data = [
        (
            "R001",
            None,
            5,
            "Excellent",
            "Very good product",
            "2018-01-01 10:00:00",
            "2018-01-02 11:00:00"
        ),
        (
            "R002",
            "O002",
            4,
            "Good",
            "Nice",
            "2018-01-03 10:00:00",
            "2018-01-04 11:00:00"
        )
    ]

    columns = [
        "review_id",
        "order_id",
        "review_score",
        "review_comment_title",
        "review_comment_message",
        "review_creation_date",
        "review_answer_timestamp"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_order_reviews(df)

    assert result.count() == 1
    assert result.first().order_id == "O002"
    

def test_timestamp_conversion(spark):

    data = [
        (
            "R001",
            "O001",
            5,
            "Excellent",
            "Very good product",
            "2018-01-01 10:00:00",
            "2018-01-02 11:00:00"
        )
    ]

    columns = [
        "review_id",
        "order_id",
        "review_score",
        "review_comment_title",
        "review_comment_message",
        "review_creation_date",
        "review_answer_timestamp"
    ]

    df = spark.createDataFrame(data, columns)

    result = transform_order_reviews(df)

    schema = result.schema

    assert isinstance(
        schema["review_creation_date"].dataType,
        TimestampType
    )

    assert isinstance(
        schema["review_answer_timestamp"].dataType,
        TimestampType
    )