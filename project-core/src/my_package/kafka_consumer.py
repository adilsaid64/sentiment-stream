from kafka import KafkaConsumer
from interface import MessageConsumerStrategy

class KafkaConsumerStrategy(MessageConsumerStrategy):
    def __init__(self, bootstrap_servers : str, topic : str, group_id:str):
        self.consumer = KafkaConsumer(topic, bootstrap_servers = bootstrap_servers, group_id = group_id)

    def consume_message(self):
        for message in self.consumer:
            yield message.value

    def close(self):
        self.consumer.close()