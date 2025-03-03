import os
import subprocess
from time import sleep
from random import randint,choice
from Constants import Constants

class GameOverException(Exception):
    pass

class Unit:

    Units:dict[Constants,list['Unit']] = {Constants.Friendly:[],Constants.Hostile:[],Constants.Passive:[]}

    def __init__(self,Damage:int,MaxHealth:int,Team:Constants):
        Unit.Units[Team].append(self)
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
    def Strongest(cls,Team:Constants) -> 'Unit':
         Damages = {}
         for Enemy in cls.Units[Team]:
             if Enemy.Alive:
                Damages[Enemy.Damage] = Enemy
         Strongest = max(Damages)
         return Damages[Strongest]

    @classmethod
    def Weakest(cls,Team:Constants) -> 'Unit':
        Healths = {}
        for Enemy in cls.Units[Team]:
            if Enemy.Alive:
                Healths[Enemy.Health] = Enemy
        Weakest = min(Healths)
        return Healths[Weakest]

    # Might change if enemy AI is changed
    # Healths dictionary was here before, might be useful
    @classmethod
    def Health(cls,Team):
        HealthTotal = 0
        MaxTotal = 0
        for Unit in cls.Units[Team]:
            HealthTotal += Unit.Health
            MaxTotal += Unit.MaxHealth
        return (HealthTotal,MaxTotal)
    
    @classmethod
    def Check(cls,Team:Constants = Constants.All):
        if Team == Constants.All:
            for Team in cls.Units:
                for Unit in cls.Units[Team]:
                    if Unit.Health <= 0:
                        Unit.Alive = False
                        cls.Units[Team].remove(Unit)
        else:
            for Unit in cls.Units[Team]:
                if Unit.Health <= 0:
                    Unit.Alive = False
                    cls.Units[Team].remove(Unit)
        if len(cls.Units[Constants.Friendly]) == 0:
            raise GameOverException("Friendly Units Win!")
        elif len(cls.Units[Constants.Hostile]) == 0:
            raise GameOverException("Hostile Units Win!")  

    #This...doesn't work,Why?
    @classmethod
    def Create(cls,Amount:int,Teams:list[Constants] = Constants.All):
        if Teams == Constants.All:
            for ATeam in cls.Units:
                for i in range(Amount):
                    cls.Units[ATeam].append(Unit(randint(4,7),randint(14,20),ATeam))
                    print(len(cls.Units[ATeam]))
        else:
            for Team in Teams:
                for i in range(Amount):
                    cls.Units[Team].append(Unit(randint(4,7),randint(14,20),Team))
                    print(len(cls.Units[Team]))

    @classmethod #ur a dumb ass bitch
    def Display(cls,Teams:list[Constants] = Constants.All):
        if Teams == Constants.All:
            for ATeam in cls.Units:
                print("-" * 28)
                print(f"{ATeam.name} Units: {len(cls.Units[ATeam])}/3")
                for AUnit in cls.Units[ATeam]:
                    print(f"Unit {cls.Units[ATeam].index(AUnit) + 1}: Health: {AUnit.Health}/{AUnit.MaxHealth}, Damage: {AUnit.Damage}")
                print("-" * 28,"\n")
                sleep(1)
        else:
            for Team in Teams:
                print("-" * 28)
                print(f"{Team.name} Units: {len(cls.Units[Team])}/3")
                for Unit in cls.Units[Team]:
                    print(f"Unit {cls.Units[Team].index(Unit) + 1}: Health: {Unit.Health}/{Unit.MaxHealth}, Damage: {Unit.Damage}")
                print("-" * 28,"\n")
                sleep(1)

# Make Useful 
class Controller:
    
    def __init__(self,Team):
        self.Team = Team

# Might merge with future enemy class
def Chance(Probability:int):
    Result = randint(1,100)
    if Result <= Probability:
        return True
    return False

def Starter() -> bool:
    Coin = randint(0,1)
    Valid = [0,1]
    while True:
        try:
            Guess = int(input("Guess the coin flip! 0 or 1: "))
            if Guess in Valid:
                break
            print("Invalid input,please try again.")
        except ValueError:
            print("Invalid input,please try again.")
    if Guess == Coin:
        print("You guessed correctly! You start.\n")
        return True
    print("You guessed incorrectly! Enemy starts.\n")
    return False

def Pause(Message:str = "Press any key to continue."):
    if os.name == "nt":
        print(Message)
        os.system("pause")
    else:
        subprocess.run(f"read -p '{Message}'",shell = True)

def Clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def Main():
    print("QTBS: First Concept.")
    print("Setting Up...")

    Unit.Create(2,[Constants.Friendly,Constants.Hostile])
    # Player = Controller(Constants.Friendly)
    # Enemy = Controller(Constants.Hostile)

    for i in range(3):
        print("...")
        sleep(1)
    
    print("Ready!")
    sleep(1)
    Clear()

    print("Welcome to QTBS!")
    sleep(1)
    Turn = Starter()
    sleep(1)
    Clear()
    Clearer = 0
    sleep(1)
    Sides = {"E":Constants.Hostile,"F":Constants.Friendly}

    while True:
        try:
            Unit.Check()
        except GameOverException as Winner:
            print(Winner)
            break
        Unit.Display([Constants.Friendly,Constants.Hostile])
        sleep(1)
        if Turn:
            print("Player's Turn:")
            while True:
                try:
                    Side = input("Enter the side you want to target, Enemy(E) or Friendly(F): ").capitalize()
                    Side = Sides[Side]
                    break
                except KeyError:
                    print("Invalid input, please try again.")
            while True:
                try:
                    TargetIndex = int(input("Enter the number of the unit you want to attack: "))
                    if TargetIndex not in range(1,len(Unit.Units[Side]) + 1):
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid input, please try again.")
            while True:
                try:
                    AttackerIndex = int(input("Enter the number of the unit you want to attack with: "))
                    if AttackerIndex not in range(1,len(Unit.Units[Constants.Friendly]) + 1):
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid input, please try again.")
            Attacker = Unit.Units[Constants.Friendly][AttackerIndex - 1]
            Target = Unit.Units[Side][TargetIndex - 1]
            Attacker.Attack(Target)
            if Side == Constants.Hostile:
                print(f"\nYou Attacked Unit {TargetIndex} with Unit {AttackerIndex} and dealt {Attacker.Damage} damage.\n")
                if not Target.Alive:
                    print(f"You have killed Unit {TargetIndex}!\n")
            else:
                print(f"\nYou Healed Unit {Target} with Unit {Attacker} and healed {Unit.FriendlyUnits[Attacker - 1].Damage} health.\n")
            sleep(1)

        else:
            print("Enemy's Turn:")
            Ratio = Unit.Health(Constants.Hostile)
            Ratio = round(Ratio[0]/Ratio[1],2) * 100
            Attack = Chance(Ratio)
            Strongest = Unit.Strongest(Constants.Hostile)
            StrongestIndex:int = (Unit.HostileUnits.index(Strongest) + 1)
            if Attack:
                Target = choice(Unit.Units[Constants.Friendly])
                TargetIndex = (Unit.FriendlyUnits.index(Target) + 1)
                Strongest.Attack(Target)
                sleep(2)
                print(f"Enemy Attacked Unit {TargetIndex} with Unit {StrongestIndex},dealt {Strongest.Damage} damage.\n")
                sleep(1)
                if not Target.Alive:
                    print(f"The Enemy has killed Unit {TargetIndex}!\n")
                sleep(1)
            else:
                Weakest = Unit.Weakest(Constants.Hostile)
                WeakestIndex = (Unit.HostileUnits.index(Weakest) + 1)
                Strongest.Attack(Weakest)
                sleep(2)
                print(f"Enemy Healed Unit {WeakestIndex} with Unit {StrongestIndex},healed {Strongest.Damage} health.\n")
                sleep(1)
        
        Turn = not Turn
        Unit.Check()
        Clearer += 1
        if Clearer % 2 == 0:
            sleep(2)
            Clear()
            Clearer = 0
    
    print("Thank you for playing QTBS!")
    sleep(1)
    exit()

Main()