from src.kafka_consumer import KafkaConsumerStrategy
from src.context import MessageConsumer
from src.utils import consume_data

if __name__ == "__main__":

    BOOTSTRAP_SERVERS : str = "broker:29092"
    TOPIC : str = "processed-data"
    GROUP_ID : str = "kafka-minio"

    consumer = MessageConsumer(KafkaConsumerStrategy(topic = TOPIC, bootstrap_servers=BOOTSTRAP_SERVERS, group_id=GROUP_ID))

    # need a way that a message consumer can generate messages, then I need a nice api to then store that messsage into some type of storage or db. use boto3 directly, functional way?

    consume_data(consumer) # then this needs to be stored in minio via the boto3 api 
