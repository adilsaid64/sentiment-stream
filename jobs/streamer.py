from reddit_streamer import RedditFetcher
from kafka_producer import KafkaProducer
from dotenv import load_dotenv
import os
import json

def stream_to_kafka(data_fetcher, kafka_producer):
    for submission in data_fetcher.fetch_data():
        message = json.dumps(submission)
        print(message)
        kafka_producer.send_message(message)


if __name__ == "__main__":
    load_dotenv()
    reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
    reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    reddit_user_agent = os.getenv('REDDIT_USER_AGENT')

    subreddit = "all"

    reddit_fetcher = RedditFetcher(reddit_client_id, reddit_client_secret, reddit_user_agent, subreddit)

    kafka_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    kafka_topic = os.getenv('KAFKA_TOPIC', 'reddit')
    kafka_producer = KafkaProducer(kafka_server=kafka_servers, topic = kafka_topic)

    stream_to_kafka(data_fetcher=reddit_fetcher, 
                    kafka_producer=kafka_producer)