from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import from_json, col, udf, rand, current_timestamp, concat_ws, randn
from pyspark.sql.types import StructType, StructField, StringType, LongType, FloatType
import pyspark.sql.functions as f
# from textblob import TextBlob

import datetime

from src.proj_logger import logger

def create_spark_session(app_name: str) -> SparkSession:
    """
    Create and configure a Spark session.
    """

    return (
        SparkSession.builder.appName(app_name)
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.4,com.redislabs:spark-redis_2.12:3.1.0") 
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "vdLPy1Qo36MrfwPumKAt") \
        .config("spark.hadoop.fs.s3a.secret.key", "W0yOZ1T6yEIMgcVLwGANEwbVs4WEqiTzfXVM3XM5") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.redis.host", "redis") \
        .config("spark.redis.port", "6379") \
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


# def analyze_sentiment(text: str) -> float:
#     if text:
#         analysis = TextBlob(text)
#         return float(analysis.sentiment.polarity)
#     return 0.0

# sentiment_udf = udf(analyze_sentiment, FloatType())

def process_twitter_batch(batch_df: DataFrame, batch_id: int) -> None:
    logger.info(f"Processing Batch ID: {batch_id} with {batch_df.count()} records")
    batch_df.printSchema()

    batch_df = batch_df.withColumn('sentiment', (rand() * 2) - 1)

    # batch_df = batch_df.withColumn('sentiment', sentiment_udf(col('comment')))

    batch_df.show(truncate=False)

    bucket_name = "twitter-data"
    write_to_bucket(batch_df=batch_df, bucket_name=bucket_name)
    logger.info(f'Wrote {batch_id} to S3')

    write_to_redis(batch_df=batch_df, table_name= 'twitter', id_column='id')
    logger.info(f'Wrote {batch_id} to Redis')


    write_to_redis_with_timestamp(batch_df=batch_df, table_name='twitter_mean', sentiment_column = 'sentiment')

    logger.info(f"Batch {batch_id} Processsed")


def process_reddit_batch(batch_df: DataFrame, batch_id: int) -> None:
    logger.info(f"Processing Batch ID: {batch_id} with {batch_df.count()} records")
    batch_df.printSchema()

    batch_df = batch_df.withColumn('sentiment', (rand() * 2) - 1)
    # batch_df = batch_df.withColumn('sentiment', sentiment_udf(col('title')))

    batch_df.show(truncate=False)

    bucket_name = "reddit-data"
    write_to_bucket(batch_df=batch_df, bucket_name=bucket_name)

    write_to_redis(batch_df=batch_df, table_name= 'reddit', id_column='id')
    logger.info(f'Wrote {batch_id} to Redis')

    write_to_redis_with_timestamp(batch_df=batch_df, table_name='reddit_mean', sentiment_column = 'sentiment')

    
    logger.info(f"Batch {batch_id} Processsed")


def write_to_bucket(batch_df:DataFrame, bucket_name:str)->None:
    now = datetime.datetime.now()
    formatted_timestamp = now.strftime("year=%Y/month=%m/day=%d/hour=%H/min=%M/sec=%S/ms=%f")
    output_path = f"s3a://{bucket_name}/output/json_data/{formatted_timestamp}"
    batch_df.write.json(output_path)
    logger.info(f"Written to Bucket: {bucket_name} - Key: {output_path}")

def write_to_redis(batch_df : DataFrame, table_name:str, id_column:str)->None:
    (batch_df.
    write.
    format("org.apache.spark.sql.redis").
    option("table", table_name).
    option("key.column", id_column).
    save(mode = 'append')
    )


def write_to_redis_with_timestamp(batch_df: DataFrame, table_name: str, sentiment_column: str) -> None:
    sentiment_mean = batch_df.agg({sentiment_column: "mean"}).collect()[0][0]
    
    mean_df = batch_df.sql_ctx.sparkSession.createDataFrame(
        [(table_name, sentiment_mean)], ["key", "value"]
    ).withColumn("timestamp", current_timestamp())
    mean_df = mean_df.withColumn("uuid", f.expr("uuid()"))

    mean_df = mean_df.withColumn("composite_key", concat_ws("::", mean_df["timestamp"], mean_df["uuid"]))

    (mean_df
     .write
     .format("org.apache.spark.sql.redis")
     .option("table", "mean_store")
     .option("key.column", "composite_key")
     .save(mode="append")
    )
