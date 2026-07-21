from gold.customer_summary import build_customer_summary
from gold.payment_summary import build_payment_summary
from gold.seller_summary import build_seller_summary
from gold.product_summary import build_product_summary

GOLD_TABLES = {
    "customer_summary": build_customer_summary,
    "payment_summary": build_payment_summary,
    "seller_summary": build_seller_summary,
    "product_summary": build_product_summary,
}