# 🏗️ Architecture

## Overview

The Lakehouse Data Platform is an end-to-end batch data engineering solution built on AWS using the Medallion Architecture. The platform ingests raw e-commerce datasets, performs distributed data transformations using Apache Spark, stores data in Delta Lake format on Amazon S3, and exposes business-ready datasets through Amazon Athena for analytics and reporting.

The pipeline is orchestrated using Apache Airflow, providing a repeatable and scheduled ETL workflow.

---

# Architecture Diagram

<p align="center">
    <img src="../assets/Lakehouse Project Architecture.png" alt="Architecture Diagram" width="100%">
</p>

---

# Design Goals

The platform was designed with the following objectives:

- Build an end-to-end batch ETL pipeline
- Implement the Medallion Architecture
- Store data using Delta Lake
- Leverage distributed processing with Apache Spark
- Orchestrate workflows using Apache Airflow
- Enable serverless analytics using Amazon Athena
- Create business-ready datasets for reporting and dashboards

---

# High-Level Workflow

```text
Raw CSV Files
        │
        ▼
Apache Spark ETL
        │
        ▼
Bronze Layer
        │
        ▼
Silver Layer
        │
        ▼
Gold Layer
        │
        ▼
Amazon S3
        │
        ▼
AWS Glue Data Catalog
        │
        ▼
Amazon Athena
        │
        ▼
Power BI / SQL Analytics
```

---

# Architecture Components

## 1. Raw Data

The pipeline starts by reading raw CSV files from the local dataset directory.

Example datasets include:

- Customers
- Orders
- Order Items
- Products
- Sellers
- Payments
- Reviews
- Geolocation

These datasets represent the operational source system.

---

## 2. Apache Spark

Apache Spark is responsible for all distributed data processing.

Responsibilities include:

- Reading CSV datasets
- Schema inference
- Data validation
- Data cleansing
- Transformations
- Business aggregations
- Writing Delta tables

Spark enables scalable processing while keeping the ETL logic modular and reusable.

---

## 3. Bronze Layer

The Bronze layer stores raw datasets in Delta Lake format without applying business logic.

### Responsibilities

- Preserve source data
- Maintain schema
- Provide a replayable raw layer
- Support downstream transformations

Characteristics:

- Raw
- Immutable
- Delta format

---

## 4. Silver Layer

The Silver layer contains cleaned and standardized datasets.

Transformations include:

- Duplicate removal
- Null value handling
- String normalization
- Data validation
- Business rule enforcement

The Silver layer serves as the trusted foundation for analytical datasets.

---

## 5. Gold Layer

The Gold layer contains denormalized summary tables optimized for analytics.

Generated tables include:

- customer_summary
- seller_summary
- product_summary
- payment_summary

These tables contain aggregated KPIs that reduce query complexity for business users.

---

## 6. Amazon S3

All Delta tables are stored in Amazon S3.

Example storage structure:

```text
s3://<bucket>/

bronze/
silver/
gold/
```

Amazon S3 acts as the centralized data lake for all Medallion layers.

---

## 7. AWS Glue Data Catalog

Only the Gold layer is registered in the AWS Glue Data Catalog.

This provides centralized metadata management and enables Athena to discover business-ready tables.

The Bronze and Silver layers remain internal to the ETL process.

---

## 8. Amazon Athena

Amazon Athena provides serverless SQL access to the Gold layer.

Analysts can query curated datasets without provisioning database infrastructure.

Example use cases include:

- Revenue analysis
- Customer analytics
- Seller performance
- Product insights

---

## 9. Power BI

Power BI connects to Amazon Athena to build interactive dashboards and reports.

Business users consume only the Gold layer, ensuring that reporting is based on validated and curated datasets.

---

# Medallion Architecture

The platform follows the Medallion Architecture pattern.

| Layer | Purpose | Consumers |
|--------|---------|-----------|
| Bronze | Raw data ingestion | Data Engineers |
| Silver | Cleaned and standardized datasets | Data Engineers |
| Gold | Business-ready analytical datasets | Analysts, BI Tools |

Each layer progressively improves data quality while preserving traceability.

---

# Data Flow

The end-to-end processing flow consists of the following stages:

1. Airflow triggers the ETL pipeline.
2. Apache Spark extracts raw CSV datasets.
3. Bronze Delta tables are created.
4. Silver transformations clean and standardize the data.
5. Gold summary tables are generated.
6. Gold tables are written to Amazon S3.
7. Gold metadata is registered in AWS Glue.
8. Amazon Athena exposes the Gold layer for querying.
9. Power BI consumes Athena for reporting.

---

# Design Decisions

## Why Apache Spark?

- Distributed processing
- Scalable ETL
- Native Delta Lake support
- Industry-standard data engineering framework

---

## Why Delta Lake?

- ACID transactions
- Efficient storage
- Schema enforcement
- Time travel support (future enhancement)

---

## Why Amazon S3?

- Durable object storage
- Low cost
- Native integration with AWS analytics services

---

## Why AWS Glue?

- Centralized metadata catalog
- Seamless integration with Athena
- Simplifies table discovery

---

## Why Amazon Athena?

- Serverless SQL engine
- No infrastructure management
- Direct querying of Delta tables stored in S3

---

# Architecture Benefits

The implemented architecture provides:

- Modular ETL design
- Clear separation of data quality stages
- Scalable distributed processing
- Reliable Delta Lake storage
- Centralized metadata management
- Serverless SQL analytics
- Business-ready reporting layer

---

# Future Improvements

Potential enhancements include:

- Streaming ingestion using Apache Kafka
- Real-time processing with Spark Structured Streaming
- Automated data quality monitoring
- CI/CD with GitHub Actions
- Infrastructure provisioning using Terraform
- Enhanced Power BI dashboards