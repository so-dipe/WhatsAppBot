from abc import ABC, abstractmethod

class ChatModel(ABC):
    @abstractmethod
    def __init__(self, model_name):
        pass
    
    @abstractmethod
    def get_chat_response(self, history, message):
        pass

    @abstractmethod
    def save_history(self, chat_id, chat_session):
        pass

    @abstractmethod
    def get_history(self, chat_id):
        pass