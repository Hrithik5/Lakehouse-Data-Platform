RELATIONSHIPS = [

    (
        "orders_dataset",
        "customers_dataset",
        "customer_id",
        "customer_id"
    ),

    (
        "order_items_dataset",
        "orders_dataset",
        "order_id",
        "order_id"
    ),

    (
        "order_items_dataset",
        "products_dataset",
        "product_id",
        "product_id"
    ),

    (
        "order_items_dataset",
        "sellers_dataset",
        "seller_id",
        "seller_id"
    ),

    (
        "order_payments_dataset",
        "orders_dataset",
        "order_id",
        "order_id"
    ),

    (
        "order_reviews_dataset",
        "orders_dataset",
        "order_id",
        "order_id"
    ),

    (
        "products_dataset",
        "product_category_name_translation",
        "product_category_name",
        "product_category_name"
    )

]