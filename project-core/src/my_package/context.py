from .interface import FetchStrategy, MessageProducerStrategy, MessageConsumerStrategy

class DataFetcher:
    def __init__(self, strategy:FetchStrategy):
        self.strategy = strategy

    def fetch(self):
        return self.strategy.fetch_data()

class MessageProducer:
    def __init__(self, strategy:MessageProducerStrategy):
        self.strategy = strategy

    def push(self, message:dict):
        self.strategy.send_message(message)


class MessageConsumer:
    def __init__(self, strategy: MessageConsumerStrategy):
        self.strategy = strategy

    def consume(self):
        return self.strategy.consume_message()