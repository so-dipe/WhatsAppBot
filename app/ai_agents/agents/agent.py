from abc import ABC, abstractmethod


class Agent(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def parse(self, prompt):
        pass

    @abstractmethod
    def respond(self, functions):
        pass
