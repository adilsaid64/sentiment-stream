from typing import Callable
import datetime
from .proj_logger import logger
from .context import DataFetcher, MessageProducer, MessageConsumer

import json
import time

def stream_data(data_fetcher:DataFetcher, message_producer:MessageProducer, sleep_time_s : int = 0):
    for submission in data_fetcher.fetch():
        message = json.dumps(submission)
        logger.info(message)
        message_producer.push(message)
        if sleep_time_s>0:time.sleep(sleep_time_s)


def consume_data_send_to_bucket(message_consumer:MessageConsumer, s3_client, bucket_name):
    for submission in message_consumer.consume():
        message_str = submission.decode('utf-8')
        message = json.loads(message_str)

        now = datetime.datetime.now()
        formatted_timestamp = now.strftime("year=%Y/month=%m/day=%d/hour=%H/min=%M/sec=%S/ms=%f")
        output_path = f"output/json_data/{formatted_timestamp}.json" 

        s3_client.put_object(
            Bucket=bucket_name,
            Key=output_path,
            Body=json.dumps(message),
            ContentType="application/json",
        )