from abc import ABC, abstractmethod
import Main
from Constants import Constants

# Important Status Effects Info:
#   - Are currently a sure hit, but will be changed to a chance to hit
#   - Are added to unit.Affected, but apllied at the end of the turn
#   - Are Missing Important Info:
#       - Duration
#       - Chance to hit
#       - Effect of stacking
#       - Synergies & Dissonances
#   - Might need an __init__ method to handle stack and potentially level in future
#   - They should also contain whether they are a buff or nerf, which has been started on below

class StatusEffect(ABC):

    #Keeping private for now, but will probaly change later tbh
    _Name:str = ""
    Sign:Constants = Constants.Null

    #Why does this need to be a property?
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
    def Apply(self,Target:'Main.Unit'):
        Target.Health -= 1