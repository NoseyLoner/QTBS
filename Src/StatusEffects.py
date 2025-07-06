from abc import ABC, abstractmethod
from Main import Unit
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

# Status Efects need a unit ID to work properly, the current system is temporary
class StatusEffect(ABC):

    #Keeping private for now, but will probaly change later tbh
    _Name:str = ""
    Sign:Constants = Constants.Null
    _Stats:dict[str:list[int]] = {}

    @property
    def Stats(self):
        for Stat in self._Stats:
            pass

    def __init__(self,Unit:'Unit', Level:int = 1, Stacks:int = 1):
        self.Unit = Unit
        self.Level = Level
        self.Stacks = Stacks

    def __eq__(self, other):
        if other.Name == self.Name:
            return True
        return False

    # Might change this to not be a property in the future
    @property
    def Name(self):
        return self._Name

    @classmethod
    @abstractmethod
    def apply(cls):
        pass

    def Stack(self,Target:'Unit'):
        if self in Target.Affected:
            Previous = Target.Affected.index(self)
            Previous.Stacks += 1

class Poison(StatusEffect):
    
    _Name = "Poison"
    Sign = Constants.Nerfs

    # Example, not suppose to be actual implementation
    def Apply(self,Target:'Unit'):
        Target.Health -= 1