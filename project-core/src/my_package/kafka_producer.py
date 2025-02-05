from src.my_package.interface import MessageProducerStrategy
from src.my_package.proj_logger import logger
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic


class KafkaProducer(MessageProducerStrategy):
    def __init__(self, kafka_server:str, topic:str):
        self.topic : str = topic

        self.producer : Producer = Producer({'bootstrap.servers':kafka_server})


    def delivery_report(self, err, msg) -> None:
        if err is not None:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def send_message(self, message)-> None:
        self.producer.produce(self.topic, message.encode('utf-8'), callback = self.delivery_report)
        self.producer.flush()


class KafkaAdmin:
    def __init__(self, kafka_server:str):
        self.kafka_server = kafka_server
        self.admin_client = AdminClient({
            "bootstrap.servers": self.kafka_server
            })
    
    def create_kafka_topic(self, topic_name:str, num_partitions:int, replication_factor:int)->None:
        topic_list = [NewTopic(topic=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)]
        try:
            futures = self.admin_client.create_topics(topic_list)
            for topic, future in futures.items():
                try:
                    future.result()
                    logger.info(f"Topic '{topic}' created successfully.")
                except Exception as e:
                    logger.error(f"Failed to create topic '{topic}': {e}")
        except Exception as e:
            logger.error(f"Error during topic creation: {e}")

        
    def delete_kafka_topic(self, topic_name:str)->None:
        try:
            futures = self.admin_client.delete_topics([topic_name])
            for topic, future in futures.items():
                try:
                    future.result()
                    logger.info(f"Topic '{topic}' deleted successfully.")
                except Exception as e:
                    logger.error(f"Failed to delete topic '{topic}': {e}")
        except Exception as e:
            logger.error(f"Error during topic deletion: {e}")

    def list_kafka_topics(self)->None:
        metadata = self.admin_client.list_topics(timeout=10)
        logger.info("Available topics:")
        for topic in metadata.topics:
            logger.info(f" - {topic}")