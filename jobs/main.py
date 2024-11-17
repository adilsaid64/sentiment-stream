from src.reddit_fetcher import RedditFetcher
from src.twitter_fetcher import TwitterFetcher
from src.kafka_producer import KafkaProducer

from src.context import  DataFetcher, MessageProducer

from dotenv import load_dotenv
import os
import json
import pandas as pd

def stream_data(data_fetcher:DataFetcher, message_producer:MessageProducer):
    for submission in data_fetcher.fetch():
        message = json.dumps(submission)
        print(message)
        message_producer.push(message)

if __name__ == "__main__":
    load_dotenv()
    reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
    reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    reddit_user_agent = os.getenv('REDDIT_USER_AGENT')

    # subreddit = "all"
    # reddit_fetcher = DataFetcher(RedditFetcher(reddit_client_id, 
    #                                            reddit_client_secret, 
    #                                            reddit_user_agent, 
    #                                            subreddit))
    
    twitter_fetcher = DataFetcher(TwitterFetcher(df = pd.read_csv('../data/twitter_dataset.csv')))

    kafka_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    kafka_topic = os.getenv('KAFKA_TOPIC', 'reddit')
    
    kafka_producer = MessageProducer(KafkaProducer(kafka_server=kafka_servers, topic = 'twitter'))

    stream_data(data_fetcher=twitter_fetcher, 
                    message_producer=kafka_producer)
    