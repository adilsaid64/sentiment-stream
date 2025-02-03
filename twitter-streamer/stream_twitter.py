from dotenv import load_dotenv
import pandas as pd

from src.my_package.twitter_fetcher import TwitterFetcher
from src.my_package.kafka_producer import KafkaProducer
from src.my_package.utils import stream_data
from src.my_package.context import  DataFetcher, MessageProducer

if __name__ == "__main__":

    load_dotenv()
    
    twitter_fetcher = DataFetcher(TwitterFetcher(df = pd.read_csv('data/twitter_dataset.csv')))
    twitter_topic = 'twitter'

    kafka_servers = 'broker:29092'
    kafka_producer = MessageProducer(KafkaProducer(kafka_server=kafka_servers, topic = twitter_topic))

    stream_data(data_fetcher=twitter_fetcher, 
                    message_producer=kafka_producer, sleep_time_s=1)
    