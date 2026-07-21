from gold.customer_summary import build_customer_summary
from gold.payment_summary import build_payment_summary
from gold.seller_summary import build_seller_summary
from confest import spark


# =============================================================================
# Payment Summary
# =============================================================================

def test_build_payment_summary(spark):

    payments = spark.createDataFrame(
        [
            ("O001", 1, "credit_card", 2, 100.0),
            ("O001", 2, "voucher", 1, 50.0),
            ("O002", 1, "boleto", 1, 75.0),
        ],
        [
            "order_id",
            "payment_sequential",
            "payment_type",
            "payment_installments",
            "payment_value",
        ],
    )

    silver = {
        "order_payments_dataset": payments
    }

    result = build_payment_summary(silver)

    assert result.count() == 2

    row = (
        result
        .filter("order_id = 'O001'")
        .first()
    )

    assert row.total_payment == 150.0
    assert row.payment_type == "credit_card"


# =============================================================================
# Customer Summary
# =============================================================================

def test_build_customer_summary(spark):

    customers = spark.createDataFrame(
        [
            ("C001", "Mumbai", "MH")
        ],
        [
            "customer_id",
            "customer_city",
            "customer_state"
        ]
    )

    orders = spark.createDataFrame(
        [
            (
                "O001",
                "C001",
                "delivered",
                "2018-01-01 10:00:00"
            ),
            (
                "O002",
                "C001",
                "delivered",
                "2018-01-02 10:00:00"
            ),
        ],
        [
            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_timestamp"
        ],
    )

    payments = spark.createDataFrame(
        [
            ("O001", 1, "credit_card", 1, 100.0),
            ("O002", 1, "boleto", 1, 200.0),
        ],
        [
            "order_id",
            "payment_sequential",
            "payment_type",
            "payment_installments",
            "payment_value",
        ],
    )

    silver = {
        "customers_dataset": customers,
        "orders_dataset": orders,
        "order_payments_dataset": payments,
    }

    result = build_customer_summary(silver)

    assert result.count() == 1

    row = result.first()

    assert row.customer_id == "C001"
    assert row.customer_city == "Mumbai"
    assert row.customer_state == "MH"

    assert row.total_orders == 2

    assert row.total_spent == 300.0

    assert row.average_order_value == 150.0


# =============================================================================
# Seller Summary
# =============================================================================

def test_build_seller_summary(spark):

    sellers = spark.createDataFrame(
        [
            ("S001", "Mumbai", "MH")
        ],
        [
            "seller_id",
            "seller_city",
            "seller_state",
        ],
    )

    order_items = spark.createDataFrame(
        [
            (
                "O001",
                1,
                "P001",
                "S001",
                "2018-01-01",
                100.0,
                20.0,
            ),
            (
                "O002",
                1,
                "P002",
                "S001",
                "2018-01-02",
                200.0,
                30.0,
            ),
        ],
        [
            "order_id",
            "order_item_id",
            "product_id",
            "seller_id",
            "shipping_limit_date",
            "price",
            "freight_value",
        ],
    )

    silver = {
        "sellers_dataset": sellers,
        "order_items_dataset": order_items,
    }

    result = build_seller_summary(silver)

    assert result.count() == 1

    row = result.first()

    assert row.seller_id == "S001"

    assert row.seller_city == "Mumbai"

    assert row.seller_state == "MH"

    assert row.total_orders == 2

    assert row.total_products_sold == 2

    assert row.total_revenue == 300.00

    assert row.total_freight == 50.00

    assert row.average_product_price == 150.00