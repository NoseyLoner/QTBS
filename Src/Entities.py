from time import sleep
from random import randint,choice
from math import floor,ceil
from Constants import Constants
from StatusEffects import StatusEffect

class Unit:

    Units:dict[Constants,list['Unit']] = {Constants.Friendly:[],Constants.Hostile:[],Constants.Passive:[]}

    # Applies argument might be redundant?
    # Might Change Health to HP
    def __init__(self,Damage:int,MaxHealth:int,Armour:int,Team:Constants,Name:str,Applies:dict[Constants,list['StatusEffect']] = {Constants.Buffs:[],Constants.Nerfs:[]}):
        Unit.Units[Team].append(self)
        self._Alive = True
        self.CanAttack:bool = True
        self.OverHeal:bool = False
        self.Damage = Damage
        self.MaxHealth = MaxHealth
        self._Health = MaxHealth
        self.Armour = Armour
        self.Team = Team
        self.Applies = Applies
        self.Name = Name
        self.Affected:list['StatusEffect'] = []
        
    @property
    def Alive(self):
        return self._Alive

    # Add stuff here when quantum part is added
    @Alive.setter
    def Alive(self,Status:bool):
        if Status:
            pass
        else:
            del self

    @property
    def Health(self):
        return self._Health
    
    # This is done for now I think
    # Floor and Ceiling need to added to deal with Targeted and Armoured
    @Health.setter
    def Health(self,Value:int):
        if Value < 0:
            self._Health -= round(Value / self.Armour)
            if self._Health <= 0:
                self._Health = 0
                self.Alive = False
        elif Value > 0:
            self._Health += Value
            if self._Health > self.MaxHealth and not self.OverHeal:
                self._Health = self.MaxHealth

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
            # When Enchantments are added, change this to allow overhealing if the unit has a certain level of mending
            if Target.Health >= Target.MaxHealth:
                # Might get rid of this message later
                print(f"{Target.Name} Cannot be healed further.")
            else:
                Target.Health += self.Damage
            # Same as above for buffs
            if self.Applies[Constants.Buffs]:
                for Effect in self.Applies[Constants.Buffs]:
                    Effect.Apply(Target)
                    Administrator.Update(Target.Team,Target.Name,f"{self.Team.value} {self.Name} has buffed {Target.Team.value} {Target.Name} with {Effect.Name}.")
            

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

    # You might want to check is the unit already applies this effect
    @classmethod
    def Imbude(cls,IUnit:'Unit',Effect:'StatusEffect'):
        IUnit.Applies[Effect.Sign].append(Effect)
