import os
from time import sleep
from random import randint,choice
from Constants import Constants
from StatusEffects import *
from Observers import Director,Controller

# Game Progress:
#   For the text based 1.0, as of now (08/03/25) mostly everything up to quantum stuff has been implemented in code, and just needs actully substance/testing:
#       - Basic game concept (Done)
#       - Status Effects (Done, ideas will be added with the quantum stuff and will be planned out in the book)
#       - Quantum Game Loop (Entanglement,(Superpositon?),Collapse) (Next)
#   (Note Quantum stuff will be planed out first in the book before any code is written, as will likely require changing everything)
#   Once all of the above is done, the only thing left is to make sure the game is actully fun (as right now it is boring, tedious and repetitive) and then release
#   Then, visuals will begin with the help of Pygame

# Important Object Orientated Programming TODO:
#     - Add Abstract Base Class (ABC's) for Status Effects (DONE)
#     - Add Singleton & Multiton Observer Pattern for Status Effect handiling and game controllers (DONE)
#     - Add Enums for Constanst (DONE)

Administrator = Director()
Player = Controller(Constants.Friendly)
Enemy = Controller(Constants.Hostile)
Administrator.Attach(Player)
Administrator.Attach(Enemy)

class GameOverException(Exception):
    pass

class Unit:

    Units:dict[Constants,list['Unit']] = {Constants.Friendly:[],Constants.Hostile:[],Constants.Passive:[]}

    # Applies argument might be redundant
    def __init__(self,Damage:int,MaxHealth:int,Team:Constants,Name:str,Applies:dict[Constants,list['StatusEffect']] = {Constants.Buffs:[],Constants.Nerfs:[]}):
        Unit.Units[Team].append(self)
        self._Alive = True
        self.Damage = Damage
        self.MaxHealth = MaxHealth
        self.Health = MaxHealth
        self.Team = Team
        self.Applies = Applies
        self.Name = Name
        self.Affected:list['StatusEffect'] = []
        
    @property
    def Alive(self):
        return self._Alive

    @Alive.setter
    def Alive(self,Status:bool):
        # Add stuff here when quantum part is added
        if Status:
            pass
        else:
            del self

    def Attack(self,Target:'Unit'):
        if Target.Team is not self.Team:
            Target.Health -= self.Damage
            Administrator.Update(Target.Team,Target.Name,f"{self.Team.value} {self.Name} has attacked {Target.Team.value} {Target.Name}.")
            # for now, status effects are sure hit, but will be chance based later on
            if self.Applies[Constants.Nerfs]:
                for Effect in self.Applies[Constants.Nerfs]:
                    Effect.Apply(Target)
                    Administrator.Update(Target.Team,Target.Name,f"{self.Team.value} {self.Name} has nerfed {Target.Team.value} {Target.Name} with {Effect.Name}.")
        else:
            Target.Health += self.Damage
            # Same as above for buffs
            if self.Applies[Constants.Buffs]:
                for Effect in self.Applies[Constants.Buffs]:
                    Effect.Apply(Target)
                    Administrator.Update(Target.Team,Target.Name,f"{self.Team.value} {self.Name} has buffed {Target.Team.value} {Target.Name} with {Effect.Name}.")
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
    def Healths(cls,Team):
        HealthTotal = 0
        MaxTotal = 0
        for Unit in cls.Units[Team]:
            HealthTotal += Unit.Health
            MaxTotal += Unit.MaxHealth
        return (HealthTotal,MaxTotal)
    
    # Change name to Collapse when quantum stuff is added
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
    def Display(cls,Teams:list[Constants] = Constants.All):
        if Teams == Constants.All:
            for ATeam in cls.Units:
                print("-" * 28)
                print(f"{ATeam.value} Units: {len(cls.Units[ATeam])}/3")
                for AUnit in cls.Units[ATeam]:
                    print(f"{AUnit.Name}: Health: {AUnit.Health}/{AUnit.MaxHealth}, Damage: {AUnit.Damage}")
                print("-" * 28,"\n")
                sleep(1)
        else:
            for Team in Teams:
                print("-" * 28)
                print(f"{Team.value} Units: {len(cls.Units[Team])}/3")
                for Unit in cls.Units[Team]:
                    print(f"{Unit.Name}: Health: {Unit.Health}/{Unit.MaxHealth}, Damage: {Unit.Damage}")
                print("-" * 28,"\n")
                sleep(1)

    # This is fine,i think?
    @classmethod
    def Create(cls,Amount:int,Team:Constants = Constants.All):
        if Team == Constants.All:
            for ATeam in cls.Units:
                for i in range(Amount):
                    cls.Units[ATeam].append(Unit(randint(4,7),randint(14,20),ATeam,f"Unit {i + 1}"))
        else:
            for i in range(Amount):
                cls.Units[Team].append(Unit(randint(4,7),randint(14,20),Team,f"Unit {i + 1}"))
                cls.Units[Team].pop()

    # If your wondering why the parametera are called Fish & Sheep, it's because i needed words that stay the same when pluralised
    # Triple nested...not sure how I feel about that
    # Yeah this code makes no f***ing sense lol
    @classmethod
    def Assign(Fish:dict[Constants,list[int]],Sheep:list['StatusEffect']):
        for Team in Fish.keys():
            FTeam = Fish[Team]
            for UnitNumber in FTeam:
                IUnit = Unit.Units[Team][UnitNumber - 1]
                for Effect in Sheep:
                    IUnit.Applies[Effect.Sign].append(Effect)

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
        print("Exiting...")
        sleep(1)
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
        
# WARNING!!!
# The main function still notifies the player of what is going on without the Administrator,controller or the 'Name' attribute of the unit class
# This MUST be change before the code can be run or any other features are added
def Main():
    print("QTBS: First Concept.")

    Unit.Create(3,Constants.Friendly)
    Unit.Create(3,Constants.Hostile)

    Tools.Wait(StartingMessage = "Setting Up...")
    
    Tutor = input("Press 'T' to play the tutorial or any other key to skip: ").capitalize()
    if Tutor == "T":
        Tools.Wait(StartingMessage = "Starting Tutorial...")
        Tools.Tutorial()

    Tools.Clear()
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
                    TargetName = int(input("Enter the number of the unit you want to target: "))
                    if TargetName not in range(1,len(Unit.Units[Side]) + 1):
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid input, please try again.")
            while True:
                try:
                    AttackerName = int(input("Enter the number of the unit you want to attack with: "))
                    if AttackerName not in range(1,len(Unit.Units[Constants.Friendly]) + 1):
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid input, please try again.")
            # There might be a better way to do this 
            Attacker = Unit.Units[Constants.Friendly][AttackerName - 1]
            Target = Unit.Units[Side][TargetName - 1]
            Attacker.Attack(Target)
            sleep(1)
            if Side == Constants.Hostile:
                print(f"\nYou Attacked {Target.Name} with Unit {Attacker.Name} and dealt {Attacker.Damage} damage.")
                if not Target.Alive:
                    print(f"You have killed {Target.Name}!")
            else:
                print(f"\nYou Healed {Target.Name} with {Attacker.Name} and healed {Attacker.Damage} health.")
            Tools.Pause()
        else:
            print("Enemy's Turn:")
            Ratio = Unit.Healths(Constants.Hostile)
            Ratio = round(Ratio[0]/Ratio[1],2) * 100
            Attack = Tools.Chance(Ratio)
            Strongest = Unit.Strongest(Constants.Hostile)
            if Attack:
                Target = choice(Unit.Units[Constants.Friendly])
                Strongest.Attack(Target)
                sleep(1)
                print(f"Enemy Attacked {Target.Name} with {Strongest.Name},dealt {Strongest.Damage} damage.")
                sleep(1)
                if not Target.Alive:
                    print(f"The Enemy has killed {Target.Name}!")
                sleep(1)
            else:
                Weakest = Unit.Weakest(Constants.Hostile)
                Strongest.Attack(Weakest)
                sleep(1)
                print(f"Enemy Healed {Weakest.Name} with {Strongest.Name},healed {Strongest.Damage} health.")
                sleep(1)
            Tools.Pause()
        
        Exit = input("Press 'E' to exit the game or any other key to continue: ").capitalize()
        if Exit == "E":
            Tools.Exit()

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

if __name__ == "__main__":
    Main()