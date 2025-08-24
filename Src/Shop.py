from Constants import Constants
from random import choice,randint
from Main import Unit
from typing import Callable
from Observers import Controller
from StatusEffects import *

class Singleton(type):
    
    Instances = {}

    def __call__(cls,*args,**kwargs):
        if cls not in cls.Instances:
            cls.Instances[cls] = super().__call__(*args,**kwargs)
        return cls.Instances[cls]

class Shop(metaclass=Singleton):

    RarityChances:dict[Constants,int] = {Constants.Legendary:7,Constants.Epic:18,Constants.Rare:30,Constants.Common:45}
    Basket:list['Upgrades'] = []

    def __init__(self,Slots:int = 2,Rarities:list[Constants] = [Constants.Common]):
        self.Shelf:list[Upgrades] = []
        self.Slots = Slots
        self.Rarities = Rarities

    # Doesn't work because:
    # 1. doesn't work if the roll is above 45
    # 2. doesn't account for not having a rarity
    def Stock(self) -> list:
        for i in range(self.Slots):
            Roll = randint(1,100)
            for Rarity in self.Rarities:
                if Roll <= self.RarityChances[Rarity]:
                    self.Shelf.append(Upgrades(Rarity))
                    break

# Below is quite possible some of the worst code I've ever written
class Upgrades:

    PossibleUpgrades:dict[Constants,list[str]] = {
        Constants.Common:["Damage","Health"],
        Constants.Rare:["Damage","MaxHealth","Heal","Armour","Health","Chance"],
        Constants.Epic:["Damage","MaxHealth","Heal","Armour","Health","Chance","AddApplies","LevelEffects","PartyIncrease"],
        Constants.Legendary:["Damage","MaxHealth","Heal","Armour","LevelEffects","Multistack","EffectSlots","PartyIncrease"]}

    ArithmeticUpgrades:dict[str,dict[Constants,dict[str,list[int | float] | float | Constants]]] = {
        "Damage":{Constants.Common:{"Values":[2,3],"Type":Constants.Additive},
                   Constants.Rare:{"Values":[4,5],"Type":Constants.Additive},
                   Constants.Epic:{"Values":[6,7],"Type":Constants.Additive},
                   Constants.Legendary:{"Values":1.50,"Type":Constants.Multiplicative}},
        "MaxHealth":{Constants.Rare:{"Values":[4,5,6],"Type":Constants.Additive},
                     Constants.Epic:{"Values":[8,9],"Type":Constants.Additive},
                     Constants.Legendary:{"Values":[1.30,1.40,1.50],"Type":Constants.Multiplicative}},
        "Heal":{Constants.Rare:{"values":[2,3],"Type":Constants.Additive},
                Constants.Epic:{"values":[4,5],"Type":Constants.Additive},
                Constants.Legendary:{"values":1.50,"Type":Constants.Multiplicative}},
        "Armour":{Constants.Rare:{"Values":1.10,"Type":Constants.Multiplicative},
                  Constants.Epic:{"Values":1.15,"Type":Constants.Multiplicative},
                  Constants.Legendary:{"Values":1.20,"Type":Constants.Multiplicative}},
        "Health":{Constants.Common:{"Values":1.15,"Type":Constants.Multiplicative},
                  Constants.Rare:{"Values":1.20,"Type":Constants.Multiplicative},
                  Constants.Epic:{"Values":1.25,"Type":Constants.Multiplicative}},
        "Chance":{Constants.Rare:{"Values":1.20,"Type":Constants.Multiplicative},
                  Constants.Epic:{"Values":1.30,"Type":Constants.Multiplicative}}}

    def __init__(self,Rarity:Constants):
        self.Rarity = Rarity
        self.Effect = choice(self.PossibleUpgrades[Rarity])
        if self.Effect in self.ArithmeticUpgrades:
            self.Value:int | float = choice(list(Upgrades.ArithmeticUpgrades[self.Effect][self.Rarity]["Values"]))
            self.Activator:Callable = self.ArithmeticActivate
        else:
            if self.Effect in ["AddApplies","LevelEffects"]:
                self.Value:StatusEffect | int = Upgrades.Evaluate(self.Effect)
            self.Activator:Callable = self.Assign()

    def __str__(self):
        if Upgrades.ArithmeticUpgrades[self.Effect][self.Rarity]["Type"] == Constants.Additive:
            return f"Increase {self.Effect} by {self.Value}"
        elif Upgrades.ArithmeticUpgrades[self.Effect][self.Rarity]["Type"] == Constants.Multiplicative:
            return f"Increase {self.Effect} by {self.Value * 100 - 100}%"
        elif self.Effect == "AddApplies":
            return f"Let's a unit apply the {self.Value.Name} Status Effect"
        elif self.Effect == "LevelEffects":
            return f"Increases the level of a Status Effect by {self.Value}"
        elif self.Effect == "Multistack":
            return f"Let's a unit stack multiple Status Effects at once"

    def ArithmeticActivate(self,Unit:Unit):
        if Upgrades.ArithmeticUpgrades[self.Effect][self.Rarity]["Type"] == Constants.Additive:
            setattr(Unit,self.Stat,getattr(Unit,self.Stat) + self.Value)
        elif Upgrades.ArithmeticUpgrades[self.Effect][self.Rarity]["Type"] == Constants.Multiplicative:
            setattr(Unit,self.Stat,getattr(Unit,self.Stat) * self.Value)

    def Evaluate(self,Evaluatee:str):
        if Evaluatee == "AddApplies":
            return choice([Burning,Weakened,Shocked,Targeted,Healing,Armoured,Frenzied])
        elif Evaluatee == "LevelEffects":
            if self.Rarity == Constants.Epic:
                return 1
            elif self.Rarity == Constants.Legendary:
                return 2
            
    def AAA(self,Applicee:Unit):
        self.Value.Applicate(Applicee)

    def LevelActivate(self,Applicee:Unit,SEName:str):
        TD:dict[str,StatusEffect] = {"Burning":Burning,"Weakened":Weakened,"Shocked":Shocked,"Targeted":Targeted,"Healing":Healing,"Armoured":Armoured,"Frenzied":Frenzied}
        Applicee.Applies[TD[SEName].Sign][TD[SEName]] += self.Value

    def MultistackActivate(self,Applicee:Unit):
        Applicee.Multistack = True

    def EffectSlotsActivate(self,Applicee:Unit):
        Applicee.EffectSlots += 1

    def PartyIncreaseActivate(self,Applicee:Controller):
        Applicee.Party += self.Value

    # Why do i have to do this again?
    def Assign(self):
        if self.Effect == "AddApplies":
            self.Activator = self.AAA
        elif self.Effect == "LevelEffects":
            self.Activator = self.LevelActivate
        elif self.Effect == "Multistack":
            self.Activator = self.MultistackActivate
        elif self.Effect == "EffectSlots":
            self.Activator = self.EffectSlotsActivate