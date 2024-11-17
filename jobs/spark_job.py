import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, LongType

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Log Spark session startup
    logger.info("Starting the Spark session and initializing Kafka stream...")

    # Initialize the Spark session with Kafka integration
    spark = SparkSession.builder.appName("RedditKafkaStreaming") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
        .getOrCreate()

    # Set log level to minimize noise
    spark.sparkContext.setLogLevel('WARN')

    # Log schema definition
    logger.info("Defining schema for 'reddit' data")

    # Define the schema for the 'reddit' data (JSON structure)
    redditSchema = StructType([
        StructField("title", StringType(), True),
        StructField("id", StringType(), True),
        StructField("url", StringType(), True),
        StructField("created_utc", LongType(), True),
        StructField("selftext", StringType(), True),
        StructField("now_time", LongType(), True)
    ])

    # Function to read data from Kafka and log the activity
    def read_kafka_topic(topic, schema):
        return (spark.readStream
                .format('kafka')
                .option('kafka.bootstrap.servers', 'broker:9092')  # Kafka broker
                .option('subscribe', topic)  # Subscribe to 'reddit' topic
                .option('startingOffsets', 'earliest')  # Read from the earliest offset
                .load()
                .selectExpr('CAST(value AS STRING)')
                .select(from_json(col('value'), schema).alias('data'))
                .select('data.*'))

    # Log Kafka data stream reading
    logger.info("Starting to read the Kafka stream...")

    # Get the streaming DataFrame from Kafka
    redditDF = read_kafka_topic('reddit', redditSchema)

    # Function to write each batch to a file
    def write_batch_to_file(batch_df, batch_id):
        # Log batch information
        logger.info(f"Batch ID: {batch_id} | Writing {batch_df.count()} records to file")
        
        # Define the output path (can use batch_id to differentiate files)
        output_path = f"/tmp/reddit_data/batch_{batch_id}.json"
        
        # Write the batch DataFrame to a JSON file (you can also use CSV or Parquet)
        batch_df.write.mode("overwrite").json(output_path)
        
        # Log completion of file write
        logger.info(f"Batch {batch_id} written to {output_path}")

    # Keep the query running and log the status
    logger.info("Streaming query started, awaiting termination...")
    # query.awaitTermination()


if __name__ == "__main__":
    # Log job startup
    logger.info("Running the main function")
    main()
