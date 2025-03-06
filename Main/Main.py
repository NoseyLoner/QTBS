import os
import subprocess
from time import sleep
from random import randint,choice
from Constants import Constants

# Important Object Orientated Programming TODO:
#     - Add Abstract Base Class (ABC's) for Status Effects
#     - Add Singleton & Multiton Observer Pattern for Status Effects
#     - Add Enums for Constanst (DONE)

# Below classes are not complete as of now, will be completed in the future for status effects
class Singleton(type):
    
    _instances = {}

    def __call__(cls,*args,**kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args,**kwargs)
        return cls._instances[cls]
    
class Multiton(type):
    pass

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
        self.StatusEffects = []
        
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

    @classmethod
    def Create(cls,Amount:int,Team:Constants = Constants.All):
        if Team == Constants.All:
            for ATeam in cls.Units:
                for i in range(Amount):
                    cls.Units[ATeam].append(Unit(randint(4,7),randint(14,20),ATeam))
        else:
            for i in range(Amount):
                cls.Units[Team].append(Unit(randint(4,7),randint(14,20),Team))
                cls.Units[Team].pop()

    @classmethod
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

class Tools:

    @staticmethod
    def Chance(Probability:int):
        Result = randint(1,100)
        if Result <= Probability:
            return True
        return False

    @staticmethod
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

    @staticmethod
    def Tutorial():
        print("Welcome to QTBS!")
        input("Every line in this tutrial is an input, so press enter to continue. ")
        input("QTBS stands for Quantum Turn Based Strategy, although right now it's just a turn based strategy. ")
        input("The game is simple, you have 3 units and so does the enemy. ")
        input("You can attack the enemy units or heal your own units. ")
        input("The enemy can do the same, and will do so based on how low it's units are. ")
        input("The game ends when either you or the enemy have no units left. ")
        input("After every turn, you can exit the game. ")
        input("After every 2 turns, you can clear the screen. ")
        input("When you're ready, press enter to start the game. ")
        Tools.Wait(StartingMessage = "Starting Game...")

    @staticmethod
    def Pause(Message:str = "Press enter to continue: "):
        if os.name == "nt":
            print(Message)
            os.system("pause")
        else:
            input(Message)

    @staticmethod
    def Clear():
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
    
    @staticmethod
    def Exit():
        Tools.Clear()
        print("Thank you for playing QTBS!")
        sleep(3)
        exit()

    @staticmethod
    def Wait(Time:int = 3,StartingMessage:str = None,Counter:str = "...",ClosingMessage:str = "Ready!"):
        if StartingMessage:
            print(StartingMessage)
        for i in range(Time):
            print(Counter)
            sleep(1)
        if ClosingMessage:
            print(ClosingMessage)
        sleep(1)
        Tools.Clear()
        
def Main():
    print("QTBS: First Concept.")
    print("Setting Up...")

    Unit.Create(3,Constants.Friendly)
    Unit.Create(3,Constants.Hostile)
    # Player = Controller(Constants.Friendly)
    # Enemy = Controller(Constants.Hostile)

    Tools.Wait()
    
    Tutor = input("Press 'T' to play the tutorial or any other key to skip: ").capitalize()
    if Tutor == "T":
        Tools.Wait(StartingMessage = "Starting Tutorial...")
        Tools.Tutorial()

    sleep(1)
    Turn = Tools.Starter()
    sleep(1)
    Tools.Clear()
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
                    TargetIndex = int(input("Enter the number of the unit you want to target: "))
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
            sleep(1)
            if Side == Constants.Hostile:
                print(f"\nYou Attacked Unit {TargetIndex} with Unit {AttackerIndex} and dealt {Attacker.Damage} damage.")
                if not Target.Alive:
                    print(f"You have killed Unit {TargetIndex}!")
            else:
                print(f"\nYou Healed Unit {Target} with Unit {Attacker} and healed {Unit.FriendlyUnits[Attacker - 1].Damage} health.")
            Tools.Pause()
        else:
            print("Enemy's Turn:")
            Ratio = Unit.Health(Constants.Hostile)
            Ratio = round(Ratio[0]/Ratio[1],2) * 100
            Attack = Tools.Chance(Ratio)
            Strongest = Unit.Strongest(Constants.Hostile)
            StrongestIndex:int = (Unit.Units[Constants.Hostile].index(Strongest) + 1)
            if Attack:
                Target = choice(Unit.Units[Constants.Friendly])
                TargetIndex = (Unit.Units[Constants.Friendly].index(Target) + 1)
                Strongest.Attack(Target)
                sleep(1)
                print(f"Enemy Attacked Unit {TargetIndex} with Unit {StrongestIndex},dealt {Strongest.Damage} damage.")
                sleep(1)
                if not Target.Alive:
                    print(f"The Enemy has killed Unit {TargetIndex}!")
                sleep(1)
            else:
                Weakest = Unit.Weakest(Constants.Hostile)
                WeakestIndex = (Unit.Units[Constants.Hostile].index(Weakest) + 1)
                Strongest.Attack(Weakest)
                sleep(1)
                print(f"Enemy Healed Unit {WeakestIndex} with Unit {StrongestIndex},healed {Strongest.Damage} health.")
                sleep(1)
            Tools.Pause()
        
        Exit = input("Press 'E' to exit the game or any other key to continue: ").capitalize()
        if Exit == "E":
            Tools.Exit()
            sleep(1)

        Turn = not Turn
        Unit.Check()
        Clearer += 1
        if Clearer % 2 == 0:
            Choice = input("Press 'C' to clear the screen or any other key to continue: ").capitalize()
            if Choice == "C":
                Tools.Clear()
                print("Screen Cleared!")
                sleep(1)
                Tools.Clear()

        print("\n")
    
    Tools.Exit()

Main()