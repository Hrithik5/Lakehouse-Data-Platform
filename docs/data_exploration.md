# Data Exploration 

1. Customer 

**Schema :** 
	root 
	|-- customer_id: string (nullable = true) 
	|-- customer_unique_id: string (nullable = true) 
	|-- customer_zip_code_prefix: integer (nullable = true) 
	|-- customer_city: string (nullable = true) 
	|-- customer_state: string (nullable = true)

**No of Columns & Rows :** 5 & 99441
PK : customer_id

2. Geolocation 

**Schema :** 
	root 
	|-- geolocation_zip_code_prefix: integer (nullable = true) 
	|-- geolocation_lat: double (nullable = true) 
	|-- geolocation_lng: double (nullable = true) 
	|-- geolocation_city: string (nullable = true) 
	|-- geolocation_state: string (nullable = true)

**No of Columns & Rows :** 5 & 1000163
PK : None

3. Order Items

**Schema :**
  root
  |-- order_id: string (nullable = true)
  |-- order_item_id: integer (nullable = true)
  |-- product_id: string (nullable = true)
  |-- seller_id: string (nullable = true)
  |-- shipping_limit_date: timestamp (nullable = true)
  |-- price: double (nullable = true)
  |-- freight_value: double (nullable = true) 

**No of Columns & Rows :** 7 & 112650
PK : (order_id, order_item_id) Composite Primary Key
FK :
- order_id → orders.order_id
- product_id → products.product_id
- seller_id → sellers.seller_id

4. Order Payments

**Schema :**
root
 |-- order_id: string (nullable = true)
 |-- payment_sequential: integer (nullable = true)
 |-- payment_type: string (nullable = true)
 |-- payment_installments: integer (nullable = true)
 |-- payment_value: double (nullable = true)

**No of Columns & Rows :** 5 & 103886
FK: order_id


5. Order Reviews

  **Schema :**
  root
  |-- review_id: string (nullable = true)
  |-- order_id: string (nullable = true)
  |-- review_score: string (nullable = true)
  |-- review_comment_title: string (nullable = true)
  |-- review_comment_message: string (nullable = true)
  |-- review_creation_date: string (nullable = true)
  |-- review_answer_timestamp: string (nullable = true)

**No of Columns & Rows :** 7 & 104162
Candidate PK : review_id [1 NULL] 
FK : order_id

6. Orders

  **Schema :**
    root
 |-- order_id: string (nullable = true)
 |-- customer_id: string (nullable = true)
 |-- order_status: string (nullable = true)
 |-- order_purchase_timestamp: timestamp (nullable = true)
 |-- order_approved_at: timestamp (nullable = true)
 |-- order_delivered_carrier_date: timestamp (nullable = true)
 |-- order_delivered_customer_date: timestamp (nullable = true)
 |-- order_estimated_delivery_date: timestamp (nullable = true)

**No of Columns & Rows :** 8 & 99441
PK : order_id
FK : customer_id

7. Product Category

**Schema :**
  root
 |-- product_category_name: string (nullable = true)
 |-- product_category_name_english: string (nullable = true)

 PK : product_category_name
 FK : products.product_category_name


**No of Columns & Rows :** 2 & 71

8. Products

**Schema :**
  root
 |-- product_id: string (nullable = true)
 |-- product_category_name: string (nullable = true)
 |-- product_name_lenght: integer (nullable = true)
 |-- product_description_lenght: integer (nullable = true)
 |-- product_photos_qty: integer (nullable = true)
 |-- product_weight_g: integer (nullable = true)
 |-- product_length_cm: integer (nullable = true)
 |-- product_height_cm: integer (nullable = true)
 |-- product_width_cm: integer (nullable = true)

**No of Columns & Rows :** 9 & 32951
PK : product_id
FK :
product_category_name
 product_category.product_category_name

9. Sellers

**Schema :**
  root
 |-- seller_id: string (nullable = true)
 |-- seller_zip_code_prefix: integer (nullable = true)
 |-- seller_city: string (nullable = true)
 |-- seller_state: string (nullable = true)

**No of Columns & Rows :** 4 & 3095
PK : seller_id


# Data Quality Section 

| Dataset          | Nulls                                         | Duplicates                           | Candidate PK                       | Candidate FK                          | Comments                                                          |
|------------------|-----------------------------------------------|--------------------------------------|------------------------------------|---------------------------------------|-------------------------------------------------------------------|
| Customers        | No significant nulls                          | None                                 | `customer_id`                      | None                                  | Clean dimension table                                             |
| Geolocation      | No major nulls                                | Expected duplicates                  | None                               | ZIP code (logical relation)           | Multiple records per ZIP code                                     |
| Orders           | Some delivery timestamps are NULL (expected)  | None                                 | `order_id`                         | `customer_id`                         | NULL delivery dates usually indicate undelivered/cancelled orders |
| Order Items      | No major nulls                                | None                                 | (`order_id`, `order_item_id`)      | `order_id`, `product_id`, `seller_id` | Composite Primary Key                                             |
| Order Payments   | No major nulls                                | Multiple rows per order (expected)   | (`order_id`, `payment_sequential`) | `order_id`                            | One order can have multiple payments                              |
| Order Reviews    | Review comments contain many NULLs (expected) | Possible duplicate `review_id` check | `review_id` (Candidate)            | `order_id`                            | Comment fields are optional                                       |
| Products         | Some product attributes & category are NULL   | None                                 | `product_id`                       | `product_category_name`               | Missing product information should be handled in Silver           |
| Sellers          | No significant nulls                          | None                                 | `seller_id`                        | None                                  | Clean dimension table                                             |
| Product Category | No nulls                                      | None                                 | `product_category_name`            | None                                  | Lookup table                                                      |



# Relationship Diagram 

```
Customers
(customer_id)
      │
      ▼
Orders
(order_id)
      │
      ├──────────────┐
      ▼              ▼
Order Items      Order Payments
      │              │
      ▼              ▼
Products        Order Reviews
      │
      ▼
Product Category

Sellers
      ▲
      │
Order Items

Geolocation
   ▲         ▲
   │         │
Customers  Sellers
 (ZIP)      (ZIP)

```

# Classify Tables 

| Dataset              | Type      |
| -------------------- | --------- |
| customers            | Dimension |
| sellers              | Dimension |
| products             | Dimension |
| orders               | Fact      |
| order_items          | Fact      |
| payments             | Fact      |
| reviews              | Fact      |
| geolocation          | Dimension |
| category_translation | Lookup    |



# Silver 

- Primary Keys → Never NULL, unique.
- Foreign Keys → Validate existence against parent tables.
- Business Attributes (city, state, category, etc.) → Decide appropriate defaults or leave NULL.
- Measurements (weight, height, price, timestamps, etc.) → Never invent values; either keep NULL or derive them.


Customer 

- PK : customer_id: 
- Business Attributes : customer_city, customer_state, customer_zipcode, customer_unique_id

# Transformation Rules
1. Remove duplicate rows
2. customer_id must not be NULL
3. customer_id must be unique
4. Replace NULL city/state with "Unknown"
5. Trim spaces from text columns

Geolocation

- BA : geolocation_zip_code_prefix, geolocation_city, geolocation_state
- Location : geolocation_lat, geolocation_lng

# Transformation Rules
1. Remove duplicate rows
2. Trim city/state names
3. Validate latitude & longitude are not NULL
4. Keep ZIP code as is

Order Items 

- PK : (order_id, order_item_id) Composite Primary Key
- FK : order_id, product_id, seller_id 
- Measurements : freight_value, price
- Date : shipping_limit_date

# Transformation Rules
1. Remove duplicate rows
2. Validate composite PK (order_id, order_item_id)
3. Validate FK (order_id, product_id, seller_id)
4. Price and freight must be ≥ 0
5. Convert shipping date to Timestamp

Order Payments

- FK : order_id
- BA : payment_type, payment_sequential
- Numeric : payment_installments
- Measurements : payment_value

# Transformation Rules
1. Remove duplicate rows
2. Validate order_id
3. Replace NULL payment_type with "Unknown"
4. Payment value must be ≥ 0

Order Reviews

- review_id is not unique in the Olist dataset and should not be treated as a primary key.
- FK : order_id
- BA : review_comment_title, review_comment_message, 
- Date : review_creation_date, review_answer_timestamp

# Transformation Rules
1. Remove duplicate rows
2. Validate review_id
3. Keep NULL review comments (they are optional)
4. Convert dates to Timestamp

Orders

- PK : order_id
- FK : customer_id
- BA : order_status, 
- Date : order_purchase_timestamp, order_approved_at, order_delivered_carrier_date,  order_delivered_customer_date, order_estimated_delivery_date

# Transformation Rules
1. Remove duplicate rows
2. Validate order_id
3. Validate customer_id
4. Convert all dates to Timestamp
5. Standardize order_status (trim + lowercase)

Product Category Translation

- PK : product_category_name
- BA : product_category_name_english

# Transformation Rules
1. Remove duplicate rows
2. Validate product_category_name
3. Trim text columns

Products

- PK : product_id
- FK : product_category_name,
- Numeric  : product_name_length, product_description_length, product_photos_qty
- Measurements :  product_weight_g, product_length_cm, product_height_cm, product_width_cm

# Transformation Rules
1. Remove duplicate rows
2. Validate product_id
3. Validate category exists
4. Keep NULL product attributes if unavailable
5. Measurements (weight, dimensions) must be ≥ 0

Seller

- PK : seller_id
- BA : seller_city, seller_state, seller_zip_code_prefix

# Transformation Rules
1. Remove duplicate rows
2. Validate seller_id
3. Replace NULL city/state with "Unknown"
4. Trim text columns

