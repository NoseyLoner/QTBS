from Constants import Constants
from random import choice
from Main import Unit
from typing import Callable
from Observers import Controller
from StatusEffects import *

class Shop:

    Rarities:dict[Constants,int] = {Constants.Common:45,Constants.Rare:30,Constants.Epic:18,Constants.Legendary:7}
    Basket:list['Upgrades'] = []

    def __init__(self,Slots:int,Rarity:Constants = Constants.Common):
        self.Slots = Slots
        self.Rarity = Rarity

    def Stock(self) -> list:
        upgrades:list[Upgrades] = []
        for i in range(self.Slots):
            pass
            # Do rarity generation logic here

class Upgrades:

    PossibleUpgrades:dict[Constants,list[str]] = {
        Constants.Common:["Damage","Health"],
        Constants.Rare:["Damage","MaxHealth","Heal","Armour","Health","Chance"],
        Constants.Epic:["Damage","MaxHealth","Heal","Armour","Health","Chance","AddApplies","LevelEffects"],
        Constants.Legendary:["Damage","MaxHealth","Heal","Armour","LevelEffects","Multistack","EffectSlots"]}

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

    OtherUpgrades:dict[str,dict[str,str | Callable[[Unit | Controller | Shop],None] | list[int]]] = {
        "AddApplies":{}
    }

    def __init__(self,Rarity:Constants,Stat:bool):
        self.Rarity = Rarity
        self.Effect = choice(self.PossibleUpgrades[Rarity])
        if self.Effect in self.ArithmeticUpgrades:
            self.Type = Constants.ArithmeticUpgrade
            self.Value:int | float = choice(list(Upgrades.ArithmeticUpgrades[self.Effect][self.Rarity]["Values"]))
            self.Activator:Callable = self.ArithmeticActivate
        elif self.Effect in ["AddApplies","LevelEffects"]:
            self.Value = Upgrades.Evaluate(self.Effect)
        

    def __str__(self):
        if Upgrades.ArithmeticUpgrades[self.Effect][self.Rarity]["Type"] == Constants.Additive:
            return f"Increase {self.Effect} by {self.Value}"
        elif Upgrades.ArithmeticUpgrades[self.Effect][self.Rarity]["Type"] == Constants.Multiplicative:
            return f"Increase {self.Effect} by {self.Value * 100 - 100}%"
        elif self.Effect == "AddApplies":
            return f"Let's a unit apply the {self.Value.Name} Status Effect"

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