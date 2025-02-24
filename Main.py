import os
from random import randint
from Constants import Constants

class Unit:

    Units = []
    HostileUnits = []
    FriendlyUnits = []
    PassiveUnits = []

    def __init__(self,Damage:int,Health:int,Team:Constants):
        Unit.Units.append(self)
        self.Alive = True
        self.Damage = Damage
        self.Health = Health
        self.Team = Team
        
    def Attack(self,Target):
        if Target.Team is not self.Team:
            Target.Health -= self.Damage
        else:
            Target.Health += self.Damage
    
    @classmethod
    def Check(cls):
        for Instance in cls.Units:
            if Instance.Health <= 0:
                Instance.Alive = False

    @classmethod
    def Split(cls):
        for Instance in cls.Units:
            if Instance.Hostile == Constants.Hostile:
                cls.HostileUnits.append(Instance)
            elif Instance.Hostile == Constants.Friendly:
                cls.FriendlyUnits.append(Instance)
            else:
                cls.PassiveUnits.append(Instance)

    @classmethod
    def Create(cls,Amount:int,Team:Constants):
        if Team == Constants.Hostile:
            for i in range(Amount):
                cls.HostileUnits.append(Unit(randint(4,7),randint(14,20),Constants.Hostile))
        elif Team == Constants.Friendly:
            for i in range(Amount):
                cls.FriendlyUnits.append(Unit(randint(4,7),randint(14,20),Constants.Friendly))
        else:
            for i in range(Amount):
                cls.FriendlyUnits.append(Unit(randint(4,7),randint(14,20),Constants.Passive))

class Controller:
    
    def __init__(self,Team):
        self.Team = Team

    
def Main():
    print("QTBS: First Concept.")
    print("Setting Up...")

    Unit.Create(3,Constants.Friendly)
    Unit.Create(3,Constants.Hostile)
    Player = Controller(Constants.Friendly)
    Enemy = Controller(Constants.Hostile)


    