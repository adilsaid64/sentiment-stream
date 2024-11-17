from confluent_kafka.admin import AdminClient, NewTopic

def create_kafka_topic(topic_name, kafka_servers, num_partitions=3, replication_factor=1):
    admin_client = AdminClient({
        "bootstrap.servers": kafka_servers
    })

    topic_list = [NewTopic(topic=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)]
    
    try:
        futures = admin_client.create_topics(topic_list)
        for topic, future in futures.items():
            try:
                future.result()
                print(f"Topic '{topic}' created successfully.")
            except Exception as e:
                print(f"Failed to create topic '{topic}': {e}")
    except Exception as e:
        print(f"Error during topic creation: {e}")

def delete_kafka_topic(topic_name, kafka_servers):
    admin_client = AdminClient({
        "bootstrap.servers": kafka_servers
    })

    try:
        futures = admin_client.delete_topics([topic_name])
        for topic, future in futures.items():
            try:
                future.result()
                print(f"Topic '{topic}' deleted successfully.")
            except Exception as e:
                print(f"Failed to delete topic '{topic}': {e}")
    except Exception as e:
        print(f"Error during topic deletion: {e}")

def list_kafka_topics(kafka_servers):
    admin_client = AdminClient({
        "bootstrap.servers": kafka_servers
    })
    
    metadata = admin_client.list_topics(timeout=10)
    
    print("Available topics:")
    for topic in metadata.topics:
        print(f" - {topic}")

kafka_servers = 'localhost:9092'
create_kafka_topic("twitter", kafka_servers)
list_kafka_topics(kafka_servers)
# delete_kafka_topic("reddit", kafka_servers)
