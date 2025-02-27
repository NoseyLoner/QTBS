import os
import time
from random import randint,choice
from Constants import Constants

class Unit:

    Units = []

    # TODO: Change these into a dictionary and/or something that uses the team constants 
    HostileUnits = [] 
    FriendlyUnits = []
    PassiveUnits = []

    def __init__(self,Damage:int,MaxHealth:int,Team:Constants):
        Unit.Units.append(self)
        self.Alive = True
        self.Damage = Damage
        self.MaxHealth = MaxHealth
        self.Health = MaxHealth
        self.Team = Team
        
    def Attack(self,Target):
        if Target.Team is not self.Team:
            Target.Health -= self.Damage
        else:
            Target.Health += self.Damage
            if Target.Health > Target.MaxHealth:
                Target.Health = Target.MaxHealth

    @classmethod
    def Strongest(cls):
         Damages = {}
         for Enemy in cls.HostileUnits:
             Damages[Enemy.Damage] = Enemy
         Strongest = max(Damages)
         return Damages[Strongest]

    @classmethod
    def Weakest(cls):
        Healths = {}
        for Enemy in cls.HostileUnits:
            Healths[Enemy.Health] = Enemy
        Weakest = min(Healths)
        return Healths[Weakest]

    # TODO: Not ready,finish later
    @classmethod
    def Health(cls,Team): # Temporary,see above: ^^^
        HealthTotal = 0
        MaxTotal = 0
        Healths = {}
        for Unit in cls.Units:
            if Unit.Team == Team:
                HealthTotal += Unit.Health
                MaxTotal += Unit.MaxHealth
                Healths[Unit.Health] = Unit.MaxHealth
        return (HealthTotal,MaxTotal)
    
    @classmethod
    def Check(cls):
        for Instance in cls.Units:
            if Instance.Health <= 0:
                Instance.Alive = False
                try:
                    cls.FriendlyUnits.remove(Instance)
                    cls.HostileUnits.remove(Instance)
                    cls.PassiveUnits.remove(Instance)
                except ValueError:
                    pass    

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

    @classmethod
    def Display(cls,Team):
        if Team == Constants.Hostile:
            print("Hostile Units")
            for i in range(len(cls.HostileUnits)):
                if cls.HostileUnits[i].Alive:
                    print(f"Unit{i + 1}:{cls.HostileUnits[i].Health}/{cls.HostileUnits[i].MaxHealth} Health,{cls.HostileUnits[i].Damage} Damage")
        elif Team == Constants.Friendly:
            print("Friendly Units")
            for i in range(len(cls.FriendlyUnits)):
                if cls.FriendlyUnits[i].Alive:
                    print(f"Unit{i + 1}:{cls.FriendlyUnits[i].Health}/{cls.FriendlyUnits[i].MaxHealth} Health,{cls.FriendlyUnits[i].Damage} Damage")
        else:
            print("Passive Units")
            for i in range(len(cls.PassiveUnits)):
                if cls.PassiveUnits[i].Alive:
                    print(f"Unit{i + 1}:{cls.PassiveUnits[i].Health}/{cls.PassiveUnits[i].MaxHealth} Health,{cls.PassiveUnits[i].Damage} Damage")
        print()

class Controller:
    
    def __init__(self,Team):
        self.Team = Team

# Might merge with future enemy class
# Might also generalise using *args
def Chance(Probability:int):
    Result = randint(1,100)
    if Result <= Probability:
        return True
    return False

def Starter():
    Coin = randint(0,1)
    Guess = int(input("Guess 0 or 1: "))
    if Guess == Coin:
        return True
    return False

    
def Main():
    print("QTBS: First Concept.")
    print("Setting Up...")

    Unit.Create(3,Constants.Friendly)
    Unit.Create(3,Constants.Hostile)
    Player = Controller(Constants.Friendly)
    Enemy = Controller(Constants.Hostile)

    for i in range(3):
        print("...")
        time.sleep(1)
    
    print("Ready!")
    os.system("clear")

    Turn = Starter()
    Sides = {"E":Constants.Hostile,"F":Constants.Friendly}

    while True:
        Unit.Display(Constants.Hostile)
        Unit.Display(Constants.Friendly)
        if Turn:
            print("Player's Turn")
            Side = input("Enter the side you want to target, Enemy(E) or Friendly(F): ").capitalize()
            Side = Sides[Side]
            Target = int(input("Enter the number of the unit you want to attack: "))
            Attacker = int(input("Enter the number of the unit you want to attack with: "))
            if Side == Constants.Hostile:
                Unit.FriendlyUnits[Attacker - 1].Attack(Unit.HostileUnits[Target - 1])
                print(f"\nYou Attacked Unit")
            else:
                Unit.FriendlyUnits[Attacker - 1].Attack(Unit.FriendlyUnits[Target - 1])
        else:
            Ratio = Unit.Health(Constants.Hostile)
            Ratio = round(Ratio[0]/Ratio[1],2) * 100
            Attack = Chance(Ratio)
            Strongest = Unit.Strongest()
            if Attack:
                Strongest.Attack(choice(Unit.FriendlyUnits))
            else:
                Weakest = Unit.Weakest()
                Strongest.Attack(Weakest)
        
        Turn = not Turn
        Unit.Check()

Main()