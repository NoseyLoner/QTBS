from abc import ABC, abstractmethod
from Main.Main import Unit

# Important Status Effects Info:
#   - Are currently a sure hit, but will be changed to a chance to hit
#   - Are added to unit.Affected, but apllied at the end of the turn
#   - Are Missing Important Info:
#       - Duration
#       - Chance to hit
#       - Effect of stacking
#       - Synergies & Dissonances
#   - Might need an __init__ method to handle stack and potentially level in future

class StatusEffect(ABC):

    _Name:str = ""

    @property
    def Name(self):
        return self._Name

    @classmethod
    @abstractmethod
    def apply(self):
        pass

class Poison(StatusEffect):
    
    _Name = "Poison"

    # Example, not suppose to be actual implementation
    def Apply(self,Target:Unit):
        Target.Health -= 1