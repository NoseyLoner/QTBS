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
             if Enemy.Alive:
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
    
    # Add a check for the team constants,and then check units on that team
    # Also add a check for individual units
    # remember to add a check for "All" constant
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
        if len(cls.HostileUnits) == 0:
            print("Friendly Units Win!")
            time.sleep(1)
            exit()
        elif len(cls.FriendlyUnits) == 0:
            print("Hostile Units Win!")
            time.sleep(1)    

    #This might be redundant, remove if no use is found
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
    def Display(cls):
        print("-" * 28)
        if len(cls.HostileUnits) != 0:
            print(f"Hostile Units: {len(cls.HostileUnits)}/3")
            for i in range(len(cls.HostileUnits)):
                if cls.HostileUnits[i].Alive:
                    print(f"Unit {i + 1}:{cls.HostileUnits[i].Health}/{cls.HostileUnits[i].MaxHealth} Health,{cls.HostileUnits[i].Damage} Damage")
        time.sleep(1)
        if len(cls.FriendlyUnits) != 0:
            print(f"\nFriendly Units: {len(cls.FriendlyUnits)}/3")
            for i in range(len(cls.FriendlyUnits)):
                if cls.FriendlyUnits[i].Alive:
                    print(f"Unit {i + 1}:{cls.FriendlyUnits[i].Health}/{cls.FriendlyUnits[i].MaxHealth} Health,{cls.FriendlyUnits[i].Damage} Damage")
        if len(cls.PassiveUnits) != 0:
            print(f"\nPassive Units: {len(cls.PassiveUnits)}/3")
            time.sleep(1)
            for i in range(len(cls.PassiveUnits)):
                if cls.PassiveUnits[i].Alive:
                    print(f"Unit {i + 1}:{cls.PassiveUnits[i].Health}/{cls.PassiveUnits[i].MaxHealth} Health,{cls.PassiveUnits[i].Damage} Damage")
        print("-" * 28,"\n")

class Controller:
    
    def __init__(self,Team):
        self.Team = Team

# Might merge with future enemy class
def Chance(Probability:int):
    Result = randint(1,100)
    if Result <= Probability:
        return True
    return False

def Starter():
    Coin = randint(0,1)
    Guess = int(input("Guess 0 or 1: "))
    if Guess == Coin:
        print("You guessed correctly! You start.\n")
        return True
    print("You guessed incorrectly! Enemy starts.\n")
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
    time.sleep(1)
    os.system("cls")

    print("Welcome to QTBS!")
    time.sleep(1)
    Turn = Starter()
    Clearer = 0
    time.sleep(1)
    Sides = {"E":Constants.Hostile,"F":Constants.Friendly}

    while True:
        Unit.Check()
        Unit.Display()
        time.sleep(1)
        if Turn:
            print("Player's Turn:")
            Side = input("Enter the side you want to target, Enemy(E) or Friendly(F): ").capitalize()
            Side = Sides[Side]
            Target = int(input("Enter the number of the unit you want to attack: "))
            Attacker = int(input("Enter the number of the unit you want to attack with: "))
            if Side == Constants.Hostile:
                Unit.FriendlyUnits[Attacker - 1].Attack(Unit.HostileUnits[Target - 1])
                print(f"\nYou Attacked Unit {Target} with Unit {Attacker} and dealt {Unit.FriendlyUnits[Attacker - 1].Damage} damage.\n")
                if not Unit.HostileUnits[Target - 1].Alive:
                    print(f"You have killed Unit {Unit.HostileUnits.index(Target) + 1}!\n")
                time.sleep(1)
            else:
                Unit.FriendlyUnits[Attacker - 1].Attack(Unit.FriendlyUnits[Target - 1])
                print(f"\nYou Healed Unit {Target} with Unit {Attacker} and healed {Unit.FriendlyUnits[Attacker - 1].Damage} health.\n")
            time.sleep(1)
        else:
            print("Enemy's Turn:")
            Ratio = Unit.Health(Constants.Hostile)
            Ratio = round(Ratio[0]/Ratio[1],2) * 100
            Attack = Chance(Ratio)
            Strongest = Unit.Strongest()
            if Attack:
                Target = choice(Unit.FriendlyUnits)
                Strongest.Attack(Target)
                time.sleep(2)
                print(f"Enemy Attacked Unit {Unit.FriendlyUnits.index(Target) + 1} with Unit {Unit.HostileUnits.index(Strongest) + 1},dealt {Strongest.Damage} damage.\n")
                time.sleep(1)
                if not Target.Alive:
                    print(f"The Enemy has killed Unit {Unit.FriendlyUnits.index(Target) + 1}!\n")
                time.sleep(1)
            else:
                Weakest = Unit.Weakest()
                Strongest.Attack(Weakest)
                time.sleep(2)
                print(f"Enemy Healed Unit {Unit.HostileUnits.index(Strongest) + 1} with Unit {Unit.HostileUnits.index(Strongest) + 1},healed {Strongest.Damage} health.\n")
                time.sleep(1)
        
        Turn = not Turn
        Unit.Check()
        Clearer += 1
        if Clearer % 2 == 0:
            time.sleep(2)
            os.system("cls")
            Clearer = 0

Main()