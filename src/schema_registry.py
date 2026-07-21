from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
    TimestampType
)

SCHEMA_REGISTRY = {

    # -------------------------------------------------------------- #
    # Customers
    # -------------------------------------------------------------- #

    "customers_dataset.csv": StructType([
        StructField("customer_id", StringType(), True),
        StructField("customer_unique_id", StringType(), True),
        StructField("customer_zip_code_prefix", IntegerType(), True),
        StructField("customer_city", StringType(), True),
        StructField("customer_state", StringType(), True),
    ]),

    # -------------------------------------------------------------- #
    # Geolocation
    # -------------------------------------------------------------- #

    "geolocation_dataset.csv": StructType([
        StructField("geolocation_zip_code_prefix", IntegerType(), True),
        StructField("geolocation_lat", DoubleType(), True),
        StructField("geolocation_lng", DoubleType(), True),
        StructField("geolocation_city", StringType(), True),
        StructField("geolocation_state", StringType(), True),
    ]),

    # -------------------------------------------------------------- #
    # Orders
    # -------------------------------------------------------------- #

    "orders_dataset.csv": StructType([
        StructField("order_id", StringType(), True),
        StructField("customer_id", StringType(), True),
        StructField("order_status", StringType(), True),
        StructField("order_purchase_timestamp", TimestampType(), True),
        StructField("order_approved_at", TimestampType(), True),
        StructField("order_delivered_carrier_date", TimestampType(), True),
        StructField("order_delivered_customer_date", TimestampType(), True),
        StructField("order_estimated_delivery_date", TimestampType(), True),
    ]),

    # -------------------------------------------------------------- #
    # Order Items
    # -------------------------------------------------------------- #

    "order_items_dataset.csv": StructType([
        StructField("order_id", StringType(), True),
        StructField("order_item_id", IntegerType(), True),
        StructField("product_id", StringType(), True),
        StructField("seller_id", StringType(), True),
        StructField("shipping_limit_date", TimestampType(), True),
        StructField("price", DoubleType(), True),
        StructField("freight_value", DoubleType(), True),
    ]),

    # -------------------------------------------------------------- #
    # Order Payments
    # -------------------------------------------------------------- #

    "order_payments_dataset.csv": StructType([
        StructField("order_id", StringType(), True),
        StructField("payment_sequential", IntegerType(), True),
        StructField("payment_type", StringType(), True),
        StructField("payment_installments", IntegerType(), True),
        StructField("payment_value", DoubleType(), True),
    ]),

    # -------------------------------------------------------------- #
    # Order Reviews
    # -------------------------------------------------------------- #

    "order_reviews_dataset.csv": StructType([
        StructField("review_id", StringType(), True),
        StructField("order_id", StringType(), True),
        StructField("review_score", IntegerType(), True),
        StructField("review_comment_title", StringType(), True),
        StructField("review_comment_message", StringType(), True),
        StructField("review_creation_date", TimestampType(), True),
        StructField("review_answer_timestamp", TimestampType(), True),
    ]),

    # -------------------------------------------------------------- #
    # Products
    # -------------------------------------------------------------- #

    "products_dataset.csv": StructType([
        StructField("product_id", StringType(), True),
        StructField("product_category_name", StringType(), True),
        StructField("product_name_lenght", IntegerType(), True),
        StructField("product_description_lenght", IntegerType(), True),
        StructField("product_photos_qty", IntegerType(), True),
        StructField("product_weight_g", DoubleType(), True),
        StructField("product_length_cm", DoubleType(), True),
        StructField("product_height_cm", DoubleType(), True),
        StructField("product_width_cm", DoubleType(), True),
    ]),

    # -------------------------------------------------------------- #
    # Sellers
    # -------------------------------------------------------------- #

    "sellers_dataset.csv": StructType([
        StructField("seller_id", StringType(), True),
        StructField("seller_zip_code_prefix", IntegerType(), True),
        StructField("seller_city", StringType(), True),
        StructField("seller_state", StringType(), True),
    ]),

    # -------------------------------------------------------------- #
    # Category Translation
    # -------------------------------------------------------------- #

    "product_category_name_translation.csv": StructType([
        StructField("product_category_name", StringType(), True),
        StructField("product_category_name_english", StringType(), True),
    ])
}