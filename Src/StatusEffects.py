import warnings
from random import choice
from Main import Unit,Tools
from Constants import Constants

class StatusEffect():
    # Add a status effect that can cure other status effects

    Name:str = ""
    Sign:Constants = Constants.Null
    Effects:list = []
    Durations:list = []
    Reversable:bool = False
    Reversables:list = []

    def __init__(self,Unit:'Unit',Level:int,Stacks:int = 1):
        self.Unit = Unit
        self.Level = Level
        self.Stacks = Stacks
        self.Turns = self.Durations[Level - 1] * Stacks
        self.Reversed:dict[str,int] = {Attribute:getattr(Unit,Attribute) for Attribute in self.Reversables}

    def Effect1(self):
        pass
    
    def Effect2(self):
        pass

    def Effect3(self):
        pass

    Effects:list = [Effect1,Effect2,Effect3]

    @classmethod
    def Apply(cls,Target:'Unit',Level:int,Stacks:int = 1):
        for Effect in Target.Affected:
            if Effect.Name == cls.Name:
                cls.Stack(Target,Effect,Level,Stacks)
                return
        Target.Affected.append(cls(Target,Level,Stacks))

    # I might have to have seperate effect procedures for each effect to get rid of permanent effects
    def Effect(self):
        self.Effects[self.Level - 1]()
        self.Turns -= 1
        if self.Turns <= 0:
            self.Remove()
            return True
    
    @classmethod
    def Stack(cls,Target:'Unit',Instance:'StatusEffect',Level:int,Stacks:int):
        if Instance.Level < Level:
            Target.Affected.remove(Instance)
            if Instance.Reversable:
                Instance.Reverse()
            del Instance
            Target.Affected.append(cls(Target,Level,Stacks))
        else:
            Instance.Turns += cls.Durations[Level - 1] * Stacks

    # Might chance name to Remove
    def Reverse(self):
        for Attribute,Value in self.Reversed.items():
            setattr(self.Unit,Attribute,Value)

    def Remove(self):
        self.Unit.Affected.remove(self)
        if self.Reversable:
            self.Reverse()
        del self

    # Dumb name
    @classmethod
    def Applicate(cls,Applicee:Unit):
        Applicee.Applies[cls.Sign][cls] = 1

# Some status effects may need additional features like unit ID or a chance system to be fully implemented
class Burning(StatusEffect):

    Name:str = "Burning"
    Sign:Constants = Constants.Nerfs
    Durations:list = [2,2,3]
    Reversable:bool = True
    Reversables:list = ["Damage"]

    # Randomly burning units is set at 15% for Burning1 & 2, and at 20% for Burning3
    def Burning1(self):
        self.Unit.Health -= 2
        if Tools.Chance(15):
            Targets = 1
            while Targets != 0:
                Possible = choice(Unit.Units[self.Unit.Team].values())
                if Possible != self.Unit:
                    Possible.Health -= 1
                    Targets -= 1

    def Burning2(self):
        self.Unit.Health -= 3
        if Tools.Chance(15):
            Targets = 1
            while Targets != 0:
                Possible = choice(Unit.Units[self.Unit.Team].values())
                if Possible != self.Unit:
                    Possible.Health -= 1
                    Targets -= 1

    # Burn chance is set at 20% for now
    Burnt:bool = False
    def Burning3(self):
        self.Unit.Health -= 4
        if Tools.Chance(20):
                Targets = 2
                while Targets != 0:
                    Possible = choice(Unit.Units[self.Unit.Team].values())
                    if Possible != self.Unit:
                        Possible.Health -= 2
                        Targets -= 1
        if self.Burnt:
            self.Unit.Damage += 1
            self.Burnt = False
        if not self.Burnt:
            if Tools.Chance(20):
                self.Unit.Damage -= 1
                self.Burnt = True

    Effects = [Burning1, Burning2, Burning3]

class Weakened(StatusEffect):

    Name:str = "Weakened"
    Sign:Constants = Constants.Nerfs
    Durations:list = [2,2,3]
    Reversable:bool = True
    Reversables:list = ["Damage"]
    
    W1:bool = False
    def Weakened1(self):
        if not self.W1:
            self.Unit.Damage -= 2
            self.W1 = True

    # Extra weaken chance is set at 20%
    # The stuff I'm going to do with W2 and W3 is probably really bad, but it avoids Weakened3 not reducing damage
    # Also the extra effect being weakening damage again by 1 is really boring and unoriginal
    W2:bool = False
    Extra:bool = False
    def Weakened2(self,Weakener:bool = W2):
        if not Weakener:
            self.Unit.Damage -= 3
            self.W2 = True
            if self.Extra:
                self.Unit.Damage += 1
                self.Extra = False
            if not self.Extra:
                if Tools.Chance(20):
                    self.Unit.Damage -= 1
                    self.Extra = True

    Counts:int = 3
    W3:bool = False
    def Weakened3(self):
        self.Weakened2(Weakener = self.W3)
        if Tools.Chance(25) and self.Counts > 0:
            self.Unit.Damage -= 1
            self.Counts -= 1

    Effects = [Weakened1, Weakened2, Weakened3]

class Shocked(StatusEffect):

    Name:str = "Shocked"
    Sign:Constants = Constants.Nerfs
    # Durations are increased as Shocking effects are chance based
    Durations:list = [7,6,5]
    Reversable:bool = False

    # Chance to deal damage is set at 20% for Shocked1 & 2, and at 25% for Shocked3
    def Shocked1(self):
        if Tools.Chance(40):
            self.Unit.Health -= 3
            self.Unit.CanAttack = False

    def Shocked2(self):
        if Tools.Chance(45):
            self.Unit.Health -= 3
            self.Unit.CanAttack = False
            if Tools.Chance(15):
                Targets = 1
                while Targets != 0:
                    Possible = choice(Unit.Units[self.Unit.Team].values())
                    if Possible != self.Unit:
                        Possible.Health -= 1
                        Targets -= 1

    def Shocked3(self):
        if Tools.Chance(50):
            self.Unit.Health -= 4
            self.Unit.CanAttack = False
            if Tools.Chance(15):
                Targets = choice([1, 2])
                while Targets != 0:
                    Possible = choice(Unit.Units[self.Unit.Team].values())
                    if Possible != self.Unit:
                        Possible.Health -= choice([1, 2])
                        Targets -= 1

    Effects = [Shocked1, Shocked2, Shocked3]

# Might rebalance this
class Targeted(StatusEffect):

    Name:str = "Targeted"
    Sign:Constants = Constants.Nerfs
    Durations:list = [4,4,4]
    Reversable:bool = True
    Reversables:list = ["Armour"]

    def Targeted1(self):
        self.Unit.Armour = round(self.Unit.Armour * 1.15,2)

    def Targeted2(self):
        self.Unit.Armour = round(self.Unit.Armour * 1.20,2)

    def Targeted3(self):
        self.Unit.Armour = round(self.Unit.Armour * 1.25,2)

    Effects = [Targeted1, Targeted2, Targeted3]

class Healing(StatusEffect):

    Name:str = "Healing"
    Sign:Constants = Constants.Buffs
    Durations:list = [3,3,3]

    def Healing1(self):
        self.Unit.Health += 3
        if self.Unit.Health > self.Unit.MaxHealth:
            self.Unit.Health = self.Unit.MaxHealth

    def Healing2(self):
        Comp1 = self.Unit.Health + 3
        Comp2 = round(self.Unit.MaxHealth * 1.15)
        self.Unit.Health = max(Comp1,Comp2)
        if self.Unit.Health > self.Unit.MaxHealth:
            self.Unit.Health = self.Unit.MaxHealth

    def Healing3(self):
        Comp1 = self.Unit.Health + 5
        Comp2 = round(self.Unit.MaxHealth * 1.25)
        self.Unit.OverHeal = True
        self.Unit.Health = max(Comp1,Comp2)
        self.Unit.OverHeal = False

    Effects = [Healing1, Healing2, Healing3]

class Armoured(StatusEffect):

    Name:str = "Armoured"
    Sign:Constants = Constants.Buffs
    Durations:list = [3,3,3]
    Reversable:bool = True
    Reversables:list = ["Armour"]

    def Armoured1(self):
        self.Unit.Armour = round(self.Unit.Armour * 1.20,2)

    def Armoured2(self):
        self.Unit.Armour = round(self.Unit.Armour * 1.25,2)

    def Armoured3(self):
        self.Unit.Armour = round(self.Unit.Armour * 1.30,2)

    Effects = [Armoured1, Armoured2, Armoured3]

class Frenzied(StatusEffect):

    Name:str = "Frenzied"
    Sign:Constants = Constants.Buffs
    Durations:list = [3,3,3]
    Reversable:bool = True
    Reversables:list = ["Damage","MaxHealth"]

    F1:bool = False
    def Frenzied1(self):
        if not self.F1:
            self.Unit.Damage = round(self.Unit.Damage * 1.1)
            self.Unit.MaxHealth = round(self.Unit.MaxHealth * 0.9)
            if self.Unit.Health > self.Unit.MaxHealth:
                self.Unit.Health = self.Unit.MaxHealth
            self.F1 = True

    F2:bool = False
    def Frenzied2(self):
        if not self.F2:
            self.Unit.Damage = round(self.Unit.Damage * 1.2)
            self.Unit.MaxHealth = round(self.Unit.MaxHealth * 0.8)
            if self.Unit.Health > self.Unit.MaxHealth:
                self.Unit.Health = self.Unit.MaxHealth
            self.F2 = True

    F3:bool = False
    def Frenzied3(self):
        if not self.F3:
            self.Unit.Damage = round(self.Unit.Damage * 1.4)
            self.Unit.MaxHealth = round(self.Unit.MaxHealth * 0.6)
            if self.Unit.Health > self.Unit.MaxHealth:
                self.Unit.Health = self.Unit.MaxHealth
            self.F3 = True

    Effects = [Frenzied1, Frenzied2, Frenzied3]