from transformations.customers import transform_customers
from transformations.sellers import transform_sellers
from transformations.category_translation import transform_product_category
from transformations.products import transform_products
from transformations.orders import transform_orders
from transformations.order_payments import transform_order_payments
from transformations.order_reviews import transform_order_reviews
from transformations.order_items import transform_order_items
from transformations.geolocation import transform_geolocation


TRANSFORMERS = {
    "customers_dataset": transform_customers,
    "sellers_dataset": transform_sellers,
    "product_category_name_translation" : transform_product_category,
    "products_dataset": transform_products,
    "orders_dataset" : transform_orders,
    "order_payments_dataset" : transform_order_payments,
    "order_reviews_dataset" : transform_order_reviews,
    "order_items_dataset" : transform_order_items,
    "geolocation_dataset" : transform_geolocation
}