from abc import ABC, abstractmethod

class FetchStrategy(ABC):
    """An interface for fetching data"""

    @abstractmethod
    def fetch_data(self):
        """Fetch data from a data source"""
        pass

class MessageProducerStrategy(ABC):
    """Interface for sending messages to a message broker"""
   
    @abstractmethod
    def send_message(self, message):
        """Send message to message broker"""
        pass