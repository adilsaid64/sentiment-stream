from src.kafka_consumer import KafkaConsumerStrategy
from src.context import MessageConsumer
from src.utils import consume_data_send_to_bucket
import boto3
from botocore.client import Config
import os

MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")

if __name__ == "__main__":


    s3_client = boto3.client(
        "s3",
        endpoint_url="http://minio:9000",
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        config=Config(signature_version="s3v4")
    )

    BUCKET_NAME = "processed-data"

    BOOTSTRAP_SERVERS : str = "broker:29092"
    TOPIC : str = "processed-data"
    GROUP_ID : str = "kafka-minio"

    consumer = MessageConsumer(KafkaConsumerStrategy(topic = TOPIC, bootstrap_servers=BOOTSTRAP_SERVERS, group_id=GROUP_ID))

    # need a way that a message consumer can generate messages, then I need a nice api to then store that messsage into some type of storage or db. use boto3 directly, functional way?

    consume_data_send_to_bucket(consumer, s3_client, BUCKET_NAME) # then this needs to be stored in minio via the boto3 api 
