from abc import ABC, abstractmethod

class DataFetcher(ABC):
    """An interface for fetching data"""

    @abstractmethod
    def fetch_data(self, limit = 5):
        """Fetch data from a data source"""
        pass

class MessageProducer(ABC):
    """Interface for sending messages to a message broker"""
    def send_message(self, message):
        """Send message to message broker"""
        pass