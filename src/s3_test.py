from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("S3 Test")
    .config(
        "spark.jars.packages",
        "org.apache.hadoop:hadoop-aws:3.4.2,"
        "software.amazon.awssdk:bundle:2.29.52"
    )
    .getOrCreate()
)

hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()

hadoop_conf.set(
    "fs.s3a.impl",
    "org.apache.hadoop.fs.s3a.S3AFileSystem"
)

# Use the AWS SDK v2 default credential chain
hadoop_conf.set(
    "fs.s3a.aws.credentials.provider",
    "software.amazon.awssdk.auth.credentials.DefaultCredentialsProvider"
)

df = (
    spark.read
    .option("header", True)
    .csv("s3a://hrithik-etl-pipeline/raw/customers_dataset.csv")
)

df.show(5, truncate=False)

spark.stop()