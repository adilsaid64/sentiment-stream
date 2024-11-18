from src.proj_logger import logger
from src.context import DataFetcher, MessageProducer

import json

def stream_data(data_fetcher:DataFetcher, message_producer:MessageProducer):
    for submission in data_fetcher.fetch():
        message = json.dumps(submission)
        logger.info(message)
        message_producer.push(message)