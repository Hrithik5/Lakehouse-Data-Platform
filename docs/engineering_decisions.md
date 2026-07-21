# ❓ Engineering FAQ

## Overview

This document explains the key engineering decisions made during the design and implementation of the Lakehouse Data Platform. Rather than describing *what* the platform does, it focuses on *why* specific architectural, technology, and design choices were made.

---

# 🏗️ Architecture Decisions

---

## Why did we choose the Medallion Architecture?

The Medallion Architecture (Bronze → Silver → Gold) provides a structured approach to improving data quality as data moves through the pipeline.

This separation allows raw data to remain unchanged while progressively producing clean, validated, and business-ready datasets.

**Benefits**

- Clear separation of responsibilities
- Easier debugging
- Improved data governance
- Reproducible pipelines
- Better support for analytics

---

## Why build a Lakehouse instead of a traditional Data Warehouse?

The objective of this project was to learn modern data engineering practices.

A Lakehouse combines the flexibility of a Data Lake with the reliability and transactional guarantees traditionally associated with Data Warehouses.

**Benefits**

- Open storage format
- Low-cost object storage
- ACID transactions
- Better scalability
- Future compatibility with Databricks

---

## Why use a layered architecture instead of processing everything in one step?

Breaking the ETL into Bronze, Silver, and Gold layers isolates responsibilities.

Instead of mixing ingestion, cleaning, and business logic together, each stage performs a single well-defined task.

This improves maintainability and simplifies debugging.

---

## Why are only Gold tables registered in AWS Glue?

Gold tables represent validated, business-ready datasets intended for analytics.

Bronze and Silver are intermediate processing layers and are not meant to be queried directly by analysts.

Registering only Gold tables keeps the catalog clean and encourages users to consume trusted data.

---

# ⚙️ Technology Decisions

---

## Why Apache Spark instead of Pandas?

Apache Spark is designed for distributed data processing and is widely used in production data engineering environments.

Although the sample dataset is relatively small, Spark was chosen to build skills that scale to larger workloads.

---

## Why Delta Lake instead of Parquet?

Delta Lake extends Parquet with additional capabilities.

These include:

- ACID transactions
- Schema enforcement
- Schema evolution
- Reliable overwrite operations
- Time Travel (future capability)

Using Delta Lake makes the platform more robust while remaining compatible with the open-source Spark ecosystem.

---

## Why Amazon S3 instead of a database?

Amazon S3 serves as the centralized data lake for the platform.

It provides durable, scalable object storage and integrates naturally with Spark, Glue, and Athena.

---

## Why Amazon Athena for querying?

Athena allows SQL queries to run directly against datasets stored in Amazon S3 without managing database infrastructure.

This keeps the analytics layer simple while remaining cost-effective.

---

## Why AWS Glue Data Catalog?

Glue acts as the metadata layer for the platform.

Instead of manually tracking datasets, Glue allows Athena and other AWS services to discover registered tables automatically.

---

## Why Apache Airflow?

Airflow provides orchestration, scheduling, monitoring, and retry capabilities.

Although this project uses a simple DAG, Airflow demonstrates how ETL workflows are managed in production environments.

---

# 🧩 Design Decisions

---

## Why use a modular project structure?

The ETL pipeline is divided into separate modules:

- Extract
- Transform
- Load
- Quality
- Configuration
- Logging

Separating concerns makes the codebase easier to understand, extend, and maintain.

---

## Why centralize configuration?

Configuration values such as paths, AWS settings, and layer locations are stored separately from business logic.

This avoids hardcoded values and makes the pipeline easier to adapt across environments.

---

## Why use centralized logging?

A single logging configuration provides consistent log formatting across all modules.

This simplifies debugging and monitoring during ETL execution.

---

## Why implement data quality checks in the Silver layer?

The Silver layer is responsible for creating trusted datasets.

Typical validations include:

- Duplicate removal
- Null handling
- Data type validation
- String standardization

Keeping these checks in Silver ensures that Gold tables are generated from clean, consistent data.

---

## Why generate business summary tables?

Business users rarely work directly with normalized transactional datasets.

Instead, the Gold layer provides denormalized summary tables that simplify analytical queries and improve reporting performance.

---

# ☁️ AWS Decisions

---

## Why store every layer in Amazon S3?

S3 serves as the central storage layer for the entire platform.

Using a single storage location simplifies the architecture while enabling seamless integration with Spark, Glue, and Athena.

---

## Why register tables using Athena instead of the Glue API?

Athena DDL statements automatically update the AWS Glue Data Catalog.

This approach simplifies metadata management and reduces the amount of custom code required.

---

## Why use AWS CLI credentials during development?

AWS CLI credentials provide a simple authentication mechanism for local development.

In production environments, IAM Roles would be the preferred authentication method.

---

# 💻 Implementation Decisions

---

## Why build a batch pipeline instead of a streaming pipeline?

The source data consists of static CSV files.

A batch architecture matches the characteristics of the dataset and avoids introducing unnecessary complexity.

Streaming technologies such as Kafka and Spark Structured Streaming are planned as future enhancements.

---

## Why infer schemas automatically?

Automatic schema inference simplifies development and reduces the amount of manual schema definition required for the sample datasets.

---

## Why preserve raw data?

Raw datasets remain unchanged in the Bronze layer.

This enables:

- Data lineage
- Auditability
- Reprocessing
- Recovery from downstream transformation errors

---

# 🚀 Project-Specific Decisions

---

## Why is the Airflow DAG a single task?

The ETL logic is already modular within the application.

Instead of splitting orchestration into many Airflow tasks, a single TaskFlow task executes the complete ETL process.

This keeps the orchestration layer simple while still demonstrating Airflow scheduling and monitoring.

---

## Why not use Databricks?

The project intentionally uses open-source Apache Spark.

This keeps the platform fully runnable in a local development environment while remaining compatible with Databricks in the future.

---

## Why not expose Bronze and Silver tables?

Bronze and Silver are implementation details of the ETL process.

Only Gold tables are intended for business users, analysts, and BI tools.

---

## Why use Delta Lake for every layer?

Maintaining a consistent storage format across Bronze, Silver, and Gold simplifies the architecture and avoids format conversions between pipeline stages.

---

# 🔮 Future Improvements

Potential enhancements include:

- CI/CD using GitHub Actions
- Infrastructure as Code using Terraform
- Incremental loading
- Change Data Capture (CDC)
- Apache Kafka integration
- Spark Structured Streaming
- Automated data quality monitoring
- Data lineage visualization
- Enhanced Power BI dashboards

---

# Guiding Engineering Principles

The project was designed around the following principles:

- Separation of concerns
- Simplicity over unnecessary complexity
- Modular architecture
- Reusable components
- Layered data processing
- Configuration over hardcoding
- Business-ready analytics
- Cloud-native design
- Maintainable codebase
- Incremental scalability


## Why weren't features such as CI/CD, Terraform, multi-task Airflow DAGs, or streaming ingestion included?

This project was intentionally scoped as a learning-focused batch data engineering platform.

The primary objective was to build a complete, functional Lakehouse pipeline while maintaining steady progress through a broader data engineering learning roadmap.

Where trade-offs were necessary, priority was given to implementing core data engineering concepts correctly rather than adding production features that would significantly increase complexity without introducing new learning outcomes.

These enhancements are identified as future improvements and can be incorporated as the project evolves.

## Why use Delta Lake across Bronze, Silver, and Gold instead of mixing file formats?

Using a single storage format across all layers keeps the architecture consistent and simplifies the ETL pipeline.

This avoids unnecessary format conversions while ensuring every layer benefits from Delta Lake features such as ACID transactions and schema enforcement.

## Why is the ETL logic separated from Apache Airflow?

The ETL pipeline was designed as a standalone Python application, with Airflow responsible only for orchestration.

This separation allows the pipeline to be executed independently for local development, testing, or future orchestration tools without changing the ETL implementation.

Keeping business logic independent of the scheduler improves maintainability, testability, and portability.