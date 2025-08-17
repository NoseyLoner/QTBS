import os
from time import sleep
from Observers import Controller
from Constants import Constants
from random import randint,choice
from math import floor,ceil 

# Game Progress:
#   For the text based 1.0, as of now (08/03/25) mostly everything up to quantum stuff has been implemented in code, and just needs actully substance/testing:
#       - Basic game concept (Done)
#       - Status Effects (Done, ideas will be added with the quantum stuff and will be planned out in the book)
#       - Quantum Game Loop (Entanglement,(Superpositon?),Collapse) (Next)
#   (Note Quantum stuff will be planed out first in the book before any code is written, as will likely require changing everything)
#   Once all of the above is done, the only thing left is to make sure the game is actully fun (as right now it is boring, tedious and repetitive) and then release
#   Then, visuals will begin with the help of Pygame

class GameOverException(Exception):
    pass

class CannotAttackException(Exception):
    pass

Player = Controller(Constants.Friendly)
Enemy = Controller(Constants.Hostile)
Controllers:dict[Constants,Controller] = {Constants.Friendly:Player,Constants.Hostile:Enemy}

# self.ID = len(Unit.Units[Team]) is a simple way to add it, but it's probably not the way you want to do it
# Although it would be easy to replace the name system with
class Unit:

    Units:dict[Constants,dict[str,'Unit']] = {Constants.Friendly:{},Constants.Hostile:{},Constants.Passive:{}}
    Counters:dict[Constants,int] = {Constants.Friendly:0,Constants.Hostile:0,Constants.Passive:0}
    IDs:list[str] = []

    # Applies argument might be redundant?
    def __init__(self,Damage:int,MaxHealth:int,Armour:int,Heal:int,ID:str,Team:Constants,Applies:dict[Constants,list] = {Constants.Buffs:[],Constants.Nerfs:[]}):
        self._Alive = True
        self.CanAttack:bool = True
        self.OverHeal:bool = False
        self.Affected:list = []
        self.Controller = Controllers[Team] 
        self.Damage = Damage
        self.MaxHealth = MaxHealth
        self._Health = MaxHealth
        self.Armour = Armour
        self.Heal = Heal
        self.ID = ID
        self.Team = Team
        self.Applies = Applies
        
    @property
    def Alive(self):
        return self._Alive

    # Add stuff here when quantum part is added
    @Alive.setter
    def Alive(self,Status:bool):
        if Status:
            pass
        else:
            Unit.Units[self.Team].pop(self.ID)
            Unit.IDs.remove(self.ID)
            del self

    @property
    def Health(self):
        return self._Health
    
    # This is done for now I think
    # Floor and Ceiling need to added to deal with Targeted and Armoured
    @Health.setter
    def Health(self,Value:int):
        if Value < self._Health:
            Difference = self._Health - Value
            self._Health -= round(Difference / self.Armour)
            if self._Health <= 0:
                self._Health = 0
                if self.Team == Constants.Friendly:
                    Enemy.Coins += 1
                else:
                    Player.Coins += 1
                self.Alive = False
        elif Value > self._Health:
            self._Health = Value
            if self._Health > self.MaxHealth and not self.OverHeal:
                self._Health = self.MaxHealth

    # Remove print statements when controller system is implemented
    def Attack(self,Target:'Unit'):
        if not self.CanAttack:
            raise CannotAttackException(f"{self.ID} cannot attack!")
        else:
            if Target.Team is not self.Team:
                Target.Health -= self.Damage
                self.Controller.Update(self.ID,f"Unit {self.ID} has attacked Unit {Target.ID}, dealing {self.Damage} damage.")
                print(f"Unit {self.ID} has attacked Unit {Target.ID}, dealing {self.Damage} damage.")
                # for now, status effects are sure hit, but will be chance based later on
                if self.Applies[Constants.Nerfs]:
                    for Effect in self.Applies[Constants.Nerfs]:
                        Effect.Apply(Target)
                        self.Controller.Update(Target.ID,f"Unit {self.ID} has nerfed Unit {Target.ID} with {Effect.Name}.")
            else:
                # When Enchantments are added, change this to allow overhealing if the unit has a certain level of mending
                if Target.Health >= Target.MaxHealth:
                    # Might get rid of this message later
                    print(f"{Target.ID} Cannot be healed further.")
                else:
                    Target.Health += self.Heal
                    print(f"Unit {self.ID} has healed Unit {Target.ID} for {self.Heal} health.")
                # Same as above for buffs
                if self.Applies[Constants.Buffs]:
                    for Effect in self.Applies[Constants.Buffs]:
                        Effect.Apply(Target)
                        self.Controller.Update(Target.ID,f"Unit {self.ID} has buffed Unit {Target.ID} with {Effect.Name}.")
                        print(f"Unit {self.ID} has buffed Unit {Target.ID} with {Effect.Name}.")

    @classmethod
    def Strongest(cls,Team:Constants) -> 'Unit':
         CUnits:list['Unit'] = cls.Units[Team].values()
         MaxDamage = 0
         MaxCUnit = None
         for CUnit in CUnits:
            if CUnit.Damage > MaxDamage:
                MaxDamage = CUnit.Damage 
                MaxCUnit = CUnit
         return MaxCUnit

    @classmethod
    def Weakest(cls,Team:Constants) -> 'Unit':  
        Healths = {}
        for Enemy in cls.Units[Team].values():
            Healths[Enemy.Health] = Enemy
        Weakest = min(Healths)
        return Healths[Weakest]

    # Might change if enemy AI is changed
    # Healths dictionary was here before, might be useful
    @classmethod
    def Healths(cls,Team):
        HealthTotal = 0
        MaxTotal = 0
        for Unit in cls.Units[Team].values():
            HealthTotal += Unit.Health
            MaxTotal += Unit.MaxHealth
        return (HealthTotal,MaxTotal)
    
    # Change name to Collapse when quantum stuff is added
    @classmethod
    def Check(cls):
        if len(cls.Units[Constants.Friendly]) == 0:
            raise GameOverException("Hostile Units Win!",Constants.Hostile)
        elif len(cls.Units[Constants.Hostile]) == 0:
            raise GameOverException("Friendly Units Win!",Constants.Friendly)

    @classmethod
    def Display(cls,Teams:list[Constants] = Constants.All):
        if Teams == Constants.All:
            for ATeam in cls.Units:
                print("-" * 28)
                print(f"{ATeam.value} Units: {len(cls.Units[ATeam])}/3")
                for AUnit in cls.Units[ATeam].values():
                    print(f"{AUnit.ID}: Health: {AUnit.Health}/{AUnit.MaxHealth}, Damage: {AUnit.Damage}")
                print("-" * 28,"\n")
                sleep(1)
        else:
            for Team in Teams:
                print("-" * 28)
                print(f"{Team.value} Units: {len(cls.Units[Team])}/3")
                for Unit in cls.Units[Team].values():
                    print(f"{Unit.ID}: Health: {Unit.Health}/{Unit.MaxHealth}, Damage: {Unit.Damage}")
                print("-" * 28,"\n")
                sleep(1)

    #TODO: Make ID creation better
    @classmethod
    def Create(cls,Amount:int,Team:Constants = Constants.All):
        if Team == Constants.All:
            for ATeam in cls.Units:
                for i in range(Amount):
                    cls.Counters[ATeam] += 1
                    ID = f"{ATeam.value[0]}{cls.Counters[ATeam]}"
                    cls.Units[ATeam][ID] = Unit(randint(6,9),randint(36,45),1,randint(0,3),ID,ATeam)
                    cls.IDs.append(ID)
        else:
            for i in range(Amount):
                cls.Counters[Team] += 1
                ID = f"{Team.value[0]}{cls.Counters[Team]}"
                cls.Units[Team][ID] = Unit(randint(6,9),randint(36,45),1,randint(0,3),ID,Team)
                cls.IDs.append(ID)
                cls.Units[Team]


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

    @staticmethod
    def Shop():
        pass

    @staticmethod
    def Loop(StartAgain = False):
        if not StartAgain:
            
            Tools.Shop()
            if len(Unit.Units[Constants.Friendly]) != 3:
                Unit.Create(3 - len(Unit.Units[Constants.Friendly]),Constants.Friendly)
            Tools.Clear()

# The main function doesn't use the Controllers to notify the player
def Main(Looping:bool = False):
    if not Looping:
        # Not the first concept anymore
        print("QTBS: First Concept.")

        Unit.Create(3,Constants.Friendly)
        Unit.Create(3,Constants.Hostile)

        Tools.Wait(StartingMessage = "Setting Up...")
        
        Tutor = input("Press 'T' to play the tutorial or any other key to skip: ").capitalize()
        if Tutor == "T":
            Tools.Wait(Time = 1,StartingMessage = "Starting Tutorial...")
            Tools.Tutorial()
            Tools.Clear()
    else:
        Tools.Loop()
    
    Turn = Tools.Starter()
    sleep(1)
    Tools.Wait(Time = 1,StartingMessage = "Starting Game...")
    Clearer = 0
    sleep(1)

    while True:
        try:
            Unit.Check()
        except GameOverException as Winner:
            Controllers[Winner.args[1]].Coins += 1
            print(Winner)
            print("You know have two options, you can\n1. Continue playing by looping, gaining coin(s) to spend on upgrades\nOr\n2. Exit the game\n")
            while True:
                Choice = input("Enter 1 to Loop or 2 to Exit: ")
                if Choice == "1":
                    Tools.Wait(StartingMessage = "Looping...")
                    Main(Looping = True)
                elif Choice == "2":
                    Tools.Exit()
                else:
                    print("Invalid choice, please try again.")
        Unit.Display([Constants.Friendly,Constants.Hostile])
        if Turn:
            print("Player's Turn:")
            while True:
                try:
                    TargetID = input("Enter the ID of the unit you want to attack/heal: ").upper()
                    if TargetID not in Unit.IDs:
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid ID, please try again.")
            while True:
                try:
                    AttackerID = input("Enter the ID of the unit you want to attack/heal with: ").upper()
                    if AttackerID not in Unit.Units[Constants.Friendly]:
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid ID, please try again.")
            Attacker = Unit.Units[Constants.Friendly][AttackerID]
            if TargetID[0] == "H":
                Target = Unit.Units[Constants.Hostile][TargetID]
            elif TargetID[0] == "F":
                Target = Unit.Units[Constants.Friendly][TargetID]
            # Unused for now
            else:
                Target = Unit.Units[Constants.Passive][TargetID]
            Attacker.Attack(Target)
            sleep(1)
        else:
            print("Enemy's Turn:")
            Ratio = Unit.Healths(Constants.Hostile)
            Ratio = round(Ratio[0]/Ratio[1],2) * 100
            Attack = Tools.Chance(Ratio)
            Strongest = Unit.Strongest(Constants.Hostile)
            if Attack:
                Target = choice(list(Unit.Units[Constants.Friendly].values()))
                Strongest.Attack(Target)
                sleep(1)
                if not Target.Alive:
                    print(f"The Enemy has killed {Target.ID}!")
                sleep(1)
            else:
                Weakest = Unit.Weakest(Constants.Hostile)
                Strongest.Attack(Weakest)
                sleep(1)
        
        Exit = input("Press 'E' to exit the game or any other key to continue: ").capitalize()
        if Exit == "E":
            Tools.Exit()

        Turn = not Turn
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