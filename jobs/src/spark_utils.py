from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StructField, StringType, LongType, FloatType
# from textblob import TextBlob

import datetime

from src.proj_logger import logger

def create_spark_session(app_name: str) -> SparkSession:
    """
    Create and configure a Spark session.
    """
    return (
        SparkSession.builder.appName(app_name)
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1")
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "vdLPy1Qo36MrfwPumKAt") \
        .config("spark.hadoop.fs.s3a.secret.key", "W0yOZ1T6yEIMgcVLwGANEwbVs4WEqiTzfXVM3XM5") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .getOrCreate()
    )


def get_reddit_schema() -> StructType:
    """
    Define the schema for the Reddit data.
    """
    return StructType(
        [
            StructField("title", StringType(), True),
            StructField("id", StringType(), True),
            StructField("url", StringType(), True),
            StructField("created_utc", LongType(), True),
            StructField("selftext", StringType(), True),
            StructField("now_time", LongType(), True),
        ]
    )


def get_twitter_schema() -> StructType:
    """
    Define the schema for the Reddit data.
    """
    return StructType(
        [
            StructField("id", StringType(), True),
            StructField("username", StringType(), True),
            StructField("comment", StringType(), True),
            StructField("title", StringType(), True),
            StructField("time", StringType(), True),
        ]
    )


def read_kafka_stream(spark: SparkSession, topic: str, schema: StructType) -> DataFrame:
    """
    Read data from Kafka topic and parse it using the given schema.
    """
    return (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "broker:9092")
        .option("subscribe", topic)
        .option("startingOffsets", "earliest")
        .load()
        .selectExpr("CAST(value AS STRING) as value")
        .select(from_json(col("value"), schema).alias("data"))
        .select("data.*")
    )


def analyze_sentiment(text: str) -> float:
    if text:
        # return TextBlob(text).sentiment.polarity
        0.2
    return 0.0

sentiment_udf = udf(analyze_sentiment, FloatType())

def process_twitter_batch(batch_df: DataFrame, batch_id: int) -> None:
    logger.info(f"Processing Batch ID: {batch_id} with {batch_df.count()} records")
    batch_df.printSchema()

    # with_sentiment = batch_df.withColumn(
    #     'sentiment_score', sentiment_udf(col('comment'))
    # )

    batch_df.show(truncate=False)
    bucket_name = "twitter-data"
    write_to_bucket(batch_df=batch_df, bucket_name=bucket_name)

    logger.info(f"Batch {batch_id} Processsed")


def process_reddit_batch(batch_df: DataFrame, batch_id: int) -> None:
    logger.info(f"Processing Batch ID: {batch_id} with {batch_df.count()} records")
    batch_df.printSchema()

    # with_sentiment = batch_df.withColumn(
    #     'sentiment_score', sentiment_udf(col('comment'))
    # )

    batch_df.show(truncate=False)
    bucket_name = "reddit-data"
    write_to_bucket(batch_df=batch_df, bucket_name=bucket_name)
    logger.info(f"Batch {batch_id} Processsed")


def write_to_bucket(batch_df:DataFrame, bucket_name:str)->None:
    now = datetime.datetime.now()
    formatted_timestamp = now.strftime("year=%Y/month=%m/day=%d/hour=%H/min=%M/sec=%S/ms=%f")
    output_path = f"s3a://{bucket_name}/output/json_data/{formatted_timestamp}"
    batch_df.write.json(output_path)
    logger.info(f"Written to Bucket: {bucket_name} - Key: {output_path}")

