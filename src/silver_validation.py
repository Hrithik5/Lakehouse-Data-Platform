from pyspark.sql.functions import col

PRIMARY_KEYS = {

    "customers_dataset": [
        "customer_id"
    ],

    "orders_dataset": [
        "order_id"
    ],

    "products_dataset": [
        "product_id"
    ],

    "sellers_dataset": [
        "seller_id"
    ],

    "product_category_name_translation": [
        "product_category_name"
    ],

    "order_items_dataset": [
        "order_id",
        "order_item_id"
    ],

}

def validate_primary_key(df, table_name, pk_columns):

    # Duplicate PK
    duplicate_count = (
        df.groupBy(pk_columns)
        .count()
        .filter(col("count") > 1)
        .count()
    )

    # NULL PK
    null_count = 0

    for column in pk_columns:
        null_count += (
            df.filter(col(column).isNull()).count()
        )

    if duplicate_count == 0 and null_count == 0:
        print(f"✓ {table_name} PK validation passed")

    else:
        print(f"✗ {table_name} PK validation failed")
        print(f"Duplicate PK : {duplicate_count}")
        print(f"NULL PK : {null_count}")