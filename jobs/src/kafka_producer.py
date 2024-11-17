from src.interface import MessageProducerStrategy
from src.proj_logger import logger
from confluent_kafka import Producer


class KafkaProducer(MessageProducerStrategy):
    def __init__(self, kafka_server, topic):
        self.topic = topic

        self.producer = Producer({'bootstrap.servers':kafka_server})


    def delivery_report(self, err, msg):
        if err is not None:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def send_message(self, message):
        self.producer.produce(self.topic, message.encode('utf-8'), callback = self.delivery_report)
        self.producer.flush()