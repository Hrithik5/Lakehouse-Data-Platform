from pathlib import Path

# =============================================================================
# Project Root
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# =============================================================================
# Storage Format
# =============================================================================

# Options:
# "parquet"
# "delta"

FILE_FORMAT = "delta"

# =============================================================================
# Storage Backend
# =============================================================================

# Options:
# "local" -> Read/Write from local filesystem
# "s3"    -> Read/Write from Amazon S3

STORAGE_BACKEND = "s3"

# =============================================================================
# Amazon S3
# =============================================================================

S3_BUCKET = "hrithik-etl-pipeline"

S3_RAW = f"s3a://{S3_BUCKET}/raw"

# Keep Parquet and Delta separate
S3_BRONZE = f"s3a://{S3_BUCKET}/bronze_delta"
S3_SILVER = f"s3a://{S3_BUCKET}/silver_delta"
S3_GOLD = f"s3a://{S3_BUCKET}/gold_delta"

# =============================================================================
# Local Storage
# =============================================================================

LOCAL_RAW = PROJECT_ROOT / "data" / "raw"

LOCAL_BRONZE = PROJECT_ROOT / "data" / "bronze_delta"
LOCAL_SILVER = PROJECT_ROOT / "data" / "silver_delta"
LOCAL_GOLD = PROJECT_ROOT / "data" / "gold_delta"

# =============================================================================
# Active Data Paths
# =============================================================================

if STORAGE_BACKEND == "local":

    RAW_DATA = str(LOCAL_RAW)

    BRONZE_DATA = str(LOCAL_BRONZE)
    SILVER_DATA = str(LOCAL_SILVER)
    GOLD_DATA = str(LOCAL_GOLD)

elif STORAGE_BACKEND == "s3":

    RAW_DATA = S3_RAW

    BRONZE_DATA = S3_BRONZE
    SILVER_DATA = S3_SILVER
    GOLD_DATA = S3_GOLD

else:

    raise ValueError(
        f"Unsupported STORAGE_BACKEND: {STORAGE_BACKEND}"
    )

# =============================================================================
# Pipeline Execution
# =============================================================================

RUN_BRONZE = True
RUN_SILVER = True

RUN_REFERENTIAL_INTEGRITY = True
RUN_SILVER_VALIDATION = True

RUN_GOLD = True

# =============================================================================
# Data Writes
# =============================================================================

WRITE_BRONZE = True
WRITE_SILVER = True
WRITE_GOLD = True

# =============================================================================
# Create Local Directories
# =============================================================================

if STORAGE_BACKEND == "local":

    for folder in (
        LOCAL_RAW,
        LOCAL_BRONZE,
        LOCAL_SILVER,
        LOCAL_GOLD,
    ):
        folder.mkdir(
            parents=True,
            exist_ok=True
        )

# =============================================================================
# AWS RELATED CONFIG
# =============================================================================

AWS_REGION = "ap-south-1"
ATHENA_DATABASE = "olist_platform"

ATHENA_OUTPUT_LOCATION = (
    f"s3://{S3_BUCKET}/athena-results/"
)