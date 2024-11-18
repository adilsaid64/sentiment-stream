from src.reddit_fetcher import RedditFetcher
from src.twitter_fetcher import TwitterFetcher
from src.kafka_producer import KafkaProducer
from src.utils import stream_data

from src.context import  DataFetcher, MessageProducer
from src.proj_logger import logger
from dotenv import load_dotenv
import os
import json
import pandas as pd


if __name__ == "__main__":
    load_dotenv()
    
    twitter_fetcher = DataFetcher(TwitterFetcher(df = pd.read_csv('data/twitter_dataset.csv')))
    twitter_topic = 'twitter'

    kafka_servers = 'broker:29092'
    kafka_producer = MessageProducer(KafkaProducer(kafka_server=kafka_servers, topic = twitter_topic))

    stream_data(data_fetcher=twitter_fetcher, 
                    message_producer=kafka_producer)
    