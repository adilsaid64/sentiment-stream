"""
docker exec sentiment-stream-spark-master-1 spark-submit --master spark://spark-master:7077 --deploy-mode client --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 /opt/bitnami/spark/jobs/twitter_job.py
"""

from src.my_package.spark_utils import logger, create_spark_session, get_twitter_schema, read_kafka_stream, process_twitter_batch
from pyspark.sql.types import StructType
from pyspark.sql import SparkSession, DataFrame

def main() -> None:
    """
    Main function to configure streaming and process batches.
    """
    logger.info("Initializing Spark session...")
    spark: SparkSession = create_spark_session("SparkTwitter")

    twitter_schema: StructType = get_twitter_schema()
    kafka_stream: DataFrame = read_kafka_stream(spark, "twitter", twitter_schema)

    logger.info("Starting stream processing...")
    query = kafka_stream.writeStream.foreachBatch(process_twitter_batch).start()

    try:
        query.awaitTermination()
    except KeyboardInterrupt:
        logger.info("Streaming interrupted by user.")
    except Exception as e:
        logger.exception("Error during streaming: %s", e)
    finally:
        spark.stop()
        logger.info("Spark session stopped.")

if __name__ == "__main__":
    main()
