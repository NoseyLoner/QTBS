from Main import Unit,Tools
from Constants import Constants
import warnings

# Important Status Effects Info:
#   - Are currently a sure hit, but will be changed to a chance to hit
#   - Are added to unit.Affected, but apllied at the end of the turn
#   - Are Missing Important Info:
#       - Duration
#       - Chance to hit
#       - Effect of stacking
#       - Synergies & Dissonances

class NotImplemented(warnings):
    pass

# Status Efects need a unit ID to work properly, the current system is temporary
# The above statement is probably not true, but unit ID is needed anyways
class StatusEffect():

    # Stats was here, but it was removed, add it back if needed
    Name:str = ""
    Sign:Constants = Constants.Null
    Effects:list = []
    Durations:list = []

    def __init__(self,Unit:'Unit', Level:int = 1, Stacks:int = 1):
        self.Unit = Unit
        self.Level = Level
        self.Stacks = Stacks
        self.Turns = self.Durations[Level - 1] * Stacks
    
    def Effect1(self):
        pass
    
    def Effect2(self):
        pass

    def Effect3(self):
        pass

    Effects = [Effect1, Effect2, Effect3]

    @classmethod
    def Apply(cls,Target:'Unit', Level:int = 1, Stacks:int = 1):
        Stack = False
        for Effect in Target.Affected:
            if isinstance(Effect,cls):
                Stack = True
                break
        if Stack:
            cls.Stack(Target,Effect,Level,Stacks)
        else:
            Target.Affected.append(cls(Target, Level, Stacks))

    def Effect(self,Target:'Unit'):
        self.Effects[self.Level - 1]()
        self.Turns -= 1
        if self.Turns <= 0:
            Target.Affected.remove(self)
            del self

    def __eq__(self, other:'StatusEffect'):
        if other.Name == self.Name:
            return True
        return False
    
    @classmethod
    def Stack(cls,Target:'Unit',Instance:'StatusEffect',Level:int,Stacks:int):
        if Instance.Level < Level:
            Target.Affected.remove(Instance)
            Target.Affected.append(cls(Target, Level, Stacks))
        else:
            Instance.Turns += cls.Durations[Level - 1] * Stacks

# Some status effects may need additional features like unit ID or a chance system to be fully implemented
class Burning(StatusEffect):

    Name:str = "Burning"
    Sign:Constants = Constants.Nerfs
    Durations:list = [2,2,3]

    # Randomly burning units isn't here yet
    def Burning1(self):
        self.Unit.Health -= 2
        warnings.warn("Chance to burn has not been implemented yet in Burning1", NotImplemented)

    def Burning2(self):
        self.Unit.Health -= 3
        warnings.warn("Chance to burn has not been implemented yet in Burning2", NotImplemented)

    # Burn chance is set at 20% for now
    Burnt:bool = False
    def Burning3(self):
        self.Unit.Health -= 4
        if self.Burnt:
            self.Unit.Damage += 1
            self.Burnt = False
        if not self.Burnt:
            if Tools.Chance(20):
                self.Unit.Damage -= 1
                self.Burnt = True
        warnings.warn("Chance to burn has not been implemented yet in Burning3, and randomly reducing damage has a temporary solution", NotImplemented)

    Effects = [Burning1, Burning2, Burning3]

class Weakened(StatusEffect):

    Name:str = "Weakened"
    Sign:Constants = Constants.Nerfs
    Durations:list = [2,2,3]
    Weakened:bool = False
    
    def Weakened1(self):
        if not self.Weakened:
            self.Unit.Damage -= 2
            self.Weakened = True

    # Extra weaken chance is set at 20%
    Extra:bool = False
    def Weakened2(self):
        if not self.Weakened:
            self.Unit.Damage -= 3
            self.Weakened = True
            if self.Extra:
                self.Unit.Damage += 1
                self.Extra = False
            if not self.Extra:
                if Tools.Chance(20):
                    self.Unit.Damage -= 1
                    self.Extra = True
        warnings.warn("Randomly reducing damage has a temporary solution in Weakened2, and as such in Weakened3", NotImplemented)

    # Permanent damage reduction is set at 15%
    def Weakened3(self):
        self.Weakened2()
        if Tools.Chance(15):
            self.Unit.Damage -= 1

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

# Changing name to Luck might make more sense
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