from interface import MessageProducer
from confluent_kafka import Producer

class KafkaProducer(MessageProducer):
    def __init__(self, kafka_server, topic):
        self.topic = topic

        self.producer = Producer({'bootstrap.servers':kafka_server})

    def send_message(self, message):
        self.producer.produce(self.topic, message.encode('utf-8'))
        self.producer.flush()