from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

from config import STORAGE_BACKEND


def create_spark() -> SparkSession:
    """
    Creates and configures the SparkSession.

    Supports:
    - Delta Lake
    - Amazon S3
    """

    builder = (
    SparkSession.builder
    .appName("End-To-End ETL Pipeline")

    # .config("spark.driver.memory", "1g")
    # .config("spark.executor.memory", "1g")
    # .config("spark.driver.maxResultSize", "512m")

    .config("spark.sql.shuffle.partitions", "2")
    .config("spark.default.parallelism", "2")

    .config("spark.sql.adaptive.enabled", "true")
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true")

    .config(
        "spark.serializer",
        "org.apache.spark.serializer.KryoSerializer"
    )

    .config(
        "spark.sql.extensions",
        "io.delta.sql.DeltaSparkSessionExtension"
    )

    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog"
    )
)

    # --------------------------------------------------------------- #
    # Extra packages (S3)
    # --------------------------------------------------------------- #

    extra_packages = []

    if STORAGE_BACKEND == "s3":
        extra_packages.extend([
            "org.apache.hadoop:hadoop-aws:3.4.2",
            "software.amazon.awssdk:bundle:2.29.52"
        ])

    # --------------------------------------------------------------- #
    # Build Spark Session
    # --------------------------------------------------------------- #

    spark = configure_spark_with_delta_pip(
        builder,
        extra_packages=extra_packages
    ).getOrCreate()

    # --------------------------------------------------------------- #
    # Hadoop Configuration
    # --------------------------------------------------------------- #

    if STORAGE_BACKEND == "s3":

        hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()

        hadoop_conf.set(
            "fs.s3a.impl",
            "org.apache.hadoop.fs.s3a.S3AFileSystem"
        )

        hadoop_conf.set(
            "fs.s3a.aws.credentials.provider",
            "software.amazon.awssdk.auth.credentials.DefaultCredentialsProvider"
        )

        hadoop_conf.set(
            "fs.s3a.fast.upload",
            "true"
        )

        hadoop_conf.set(
            "mapreduce.fileoutputcommitter.algorithm.version",
            "2"
        )

    return spark