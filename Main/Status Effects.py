from abc import ABC, abstractmethod
from Main.Main import Unit

class StatusEffect(ABC):

    @abstractmethod
    def __str__(self):
        pass

    @classmethod
    @abstractmethod
    def apply(self, target:Unit):
        pass

class Base(StatusEffect):
    
    def Apply(self, target:Unit):
        pass

