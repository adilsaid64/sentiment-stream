from kafka import KafkaConsumer
from .interface import MessageConsumerStrategy
from typing import Generator

class KafkaConsumerStrategy(MessageConsumerStrategy):
    def __init__(self, bootstrap_servers : str, topic : str, group_id:str):
        self.consumer : KafkaConsumer = KafkaConsumer(topic, bootstrap_servers = bootstrap_servers, group_id = group_id)

    def consume_message(self) -> Generator[bytes, None, None]:
        for message in self.consumer:
            yield message.value

    def close(self) -> None:
        self.consumer.close()