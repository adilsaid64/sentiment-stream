from src.proj_logger import logger
from src.context import DataFetcher, MessageProducer

import json
import time

def stream_data(data_fetcher:DataFetcher, message_producer:MessageProducer, sleep_time_s : int = 0):
    for submission in data_fetcher.fetch():
        message = json.dumps(submission)
        logger.info(message)
        message_producer.push(message)
        if sleep_time_s>0:time.sleep(sleep_time_s)