from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def adapt(self):
        pass
