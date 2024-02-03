from abc import ABC, abstractmethod
import json

with open("app/language_models/personalities.json", "r") as f:
    PERSONALITIES = json.load(f)


class ChatModel(ABC):
    """
    An abstaction of a chat model.

    This class is an abstract class that defines the methods that should be
    for any chat model.

    Methods:
    - get_chat_response: Get a response from the chat model
    - save_history: Save the chat history
    - get_history: Get the chat history
    - save_chat_data: Save the chat data
    - get_chat_data: Get the chat data
    """

    @abstractmethod
    def __init__(self, model_name):
        """
        Initialize the chat model.

        Parameters:
        - model_name: The name of the chat model
        """
        pass

    @abstractmethod
    def get_chat_response(self, history, message):
        """
        Get a response from the chat model.

        Parameters:
        - history: The chat history
        - message: The message to be sent to the chat model
        """
        pass

    @abstractmethod
    def save_history(self, chat_id, chat_session):
        """
        Saves the chat history usually to a redis store.

        Parameters:
        - chat_id: The id of the chat (usually the phone number)
        - chat_session: The chat session
        """
        pass

    @abstractmethod
    def get_history(self, chat_id):
        """
        Gets the chat history usually from a redis store.

        Parameters:
        - chat_id: The id of the chat (usually the phone number)
        """
        pass

    @abstractmethod
    def save_chat_data(self, chat_id, chat_session, personality=None):
        """
        Saves the chat data usually to a redis store.

        Parameters:
        - chat_id: The id of the chat (usually the phone number)
        - chat_session: The chat session
        - personality (optional): The personality of the chat model
        """
        pass

    @abstractmethod
    def get_chat_data(self, chat_id):
        """
        Gets the chat data usually from a redis store.

        Parameters:
        - chat_id: The id of the chat (usually the phone number)
        """
        pass
