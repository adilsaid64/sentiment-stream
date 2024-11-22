import logging
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, LongType


# Configure logging
logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


def create_spark_session(app_name: str) -> SparkSession:
    """
    Create and configure a Spark session.
    """
    return (
        SparkSession.builder.appName(app_name)
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1")
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


def process_batch(batch_df: DataFrame, batch_id: int) -> None:
    """
    Process each batch: log data to the console and save to a file.
    """
    logger.info(f"Processing Batch ID: {batch_id} with {batch_df.count()} records")
    batch_df.show(truncate=False)
    output_path: str = f"/tmp/reddit_data/batch_{batch_id}.json"
    batch_df.write.mode("overwrite").json(output_path)
    logger.info(f"Batch {batch_id} written to {output_path}")