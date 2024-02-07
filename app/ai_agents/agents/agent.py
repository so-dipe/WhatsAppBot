from abc import ABC, abstractmethod


class Agent(ABC):
    """
    This class defines the interface for an AI agent.
    """

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def parse(self, prompt):
        pass

    @abstractmethod
    def respond(self, functions):
        pass
