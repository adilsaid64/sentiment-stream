from src.my_package.reddit_fetcher import RedditFetcher
from src.my_package.kafka_producer import KafkaProducer
from src.my_package.utils import stream_data
from src.my_package.context import  DataFetcher, MessageProducer
from dotenv import load_dotenv
import os
import pandas as pd



if __name__ == "__main__":
    load_dotenv()
    reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
    reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    reddit_user_agent = os.getenv('REDDIT_USER_AGENT')

    subreddit = "all"
    reddit_fetcher = DataFetcher(RedditFetcher(reddit_client_id, 
                                               reddit_client_secret, 
                                               reddit_user_agent, 
                                               subreddit))
    reddit_topic = 'reddit'
    kafka_servers = 'broker:29092'
    kafka_producer = MessageProducer(KafkaProducer(kafka_server=kafka_servers, topic = reddit_topic))

    stream_data(data_fetcher=reddit_fetcher, 
                    message_producer=kafka_producer,
                    sleep_time_s=1)