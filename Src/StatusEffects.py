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
# The above statement is probably not true, but unit ID is needed anyways
class StatusEffect():

    # Stats was here, but it was removed, add it back if needed
    Name:str = ""
    Sign:Constants = Constants.Null
    Effects:list = []

    def __init__(self,Unit:'Unit', Level:int = 1, Stacks:int = 1):
        self.Unit = Unit
        self.Level = Level
        self.Stacks = Stacks
    
    def Effect1(self):
        pass
    
    def Effect2(self):
        pass

    def Effect3(self):
        pass

    Effects = [Effect1, Effect2, Effect3]

    # Might remove stack parameter
    @classmethod
    def Apply(cls,Target:'Unit', Level:int = 1, Stacks:int = 1):
        Target.Affected.append(cls(Target, Level, Stacks))

    def Effect(self,Target:'Unit'):
        self.Effects[self.Level - 1]()

    def __eq__(self, other:'StatusEffect'):
        if other.Name == self.Name:
            return True
        return False
    
    # Might adpat to handle inter-level stacking
    def Stack(self,Target:'Unit'):
        if self in Target.Affected:
            Previous = Target.Affected.index(self)
            Previous.Stacks += 1

class Burning(StatusEffect):

    Name:str = "Burning"
    Sign:Constants = Constants.Nerfs

    def Burning1(self):
        pass

    def Burning2(self):
        pass

    def Burning3(self):
        pass

    Effects = [Burning1, Burning2, Burning3]

class Weakened(StatusEffect):

    Name:str = "Weakened"
    Sign:Constants = Constants.Nerfs

    def Weakened1(self):
        pass

    def Weakened2(self):
        pass

    def Weakened3(self):
        pass

    Effects = [Weakened1, Weakened2, Weakened3]

class Shocked(StatusEffect):

    Name:str = "Shocked"
    Sign:Constants = Constants.Nerfs

    def Shocked1(self):
        pass

    def Shocked2(self):
        pass

    def Shocked3(self):
        pass

    Effects = [Shocked1, Shocked2, Shocked3]

class Targeted(StatusEffect):

    Name:str = "Targeted"
    Sign:Constants = Constants.Nerfs

    def Targeted1(self):
        pass

    def Targeted2(self):
        pass

    def Targeted3(self):
        pass

    Effects = [Targeted1, Targeted2, Targeted3]

# Changing name ti Luck might make more sense
class Lucky(StatusEffect):

    Name:str = "Lucky"
    Sign:Constants = Constants.Buffs

    def Lucky1(self):
        pass

    def Lucky2(self):
        pass

    def Lucky3(self):
        pass

    Effects = [Lucky1, Lucky2, Lucky3]

class Healing(StatusEffect):

    Name:str = "Healing"
    Sign:Constants = Constants.Buffs

    def Healing1(self):
        pass

    def Healing2(self):
        pass

    def Healing3(self):
        pass

    Effects = [Healing1, Healing2, Healing3]

class Armoured(StatusEffect):

    Name:str = "Armoured"
    Sign:Constants = Constants.Buffs

    def Armoured1(self):
        pass

    def Armoured2(self):
        pass

    def Armoured3(self):
        pass

    Effects = [Armoured1, Armoured2, Armoured3]

class Frenzied(StatusEffect):

    Name:str = "Frenzied"
    Sign:Constants = Constants.Buffs

    def Frenzied1(self):
        pass

    def Frenzied2(self):
        pass

    def Frenzied3(self):
        pass

    Effects = [Frenzied1, Frenzied2, Frenzied3]