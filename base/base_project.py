from abc import ABC, abstractmethod


class BaseProject(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def load_model(self, model_name):
        pass

    @abstractmethod
    def teach(self):
        pass

    @abstractmethod
    def predict(self):
        pass
