from Constants import Constants
from random import choice
from Main import Unit

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

    StatUpgrades = {
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

    # TODO: update init to avoid rarity errors
    def __init__(self,Rarity:Constants,Stat:bool):
        self.Rarity = Rarity
        if Stat:
            self.Stat = choice(list(LStat for LStat in list(Upgrades.StatUpgrades.keys()) if Rarity in Upgrades.StatUpgrades[LStat].keys()))
            self.Value = choice(list(Upgrades.StatUpgrades[self.Stat][self.Rarity]["Values"]))

    def __str__(self):
        if Upgrades.StatUpgrades[self.Stat][self.Rarity]["Type"] == Constants.Additive:
            return f"Increase {self.Stat} by {self.Value}"
        elif Upgrades.StatUpgrades[self.Stat][self.Rarity]["Type"] == Constants.Multiplicative:
            return f"Increase {self.Stat} by {self.Value * 100 - 100}%"

    def Activate(self,Unit:Unit):
        if Upgrades.StatUpgrades[self.Stat][self.Rarity]["Type"] == Constants.Additive:
            setattr(Unit,self.Stat,getattr(Unit,self.Stat) + self.Value)
        elif Upgrades.StatUpgrades[self.Stat][self.Rarity]["Type"] == Constants.Multiplicative:
            setattr(Unit,self.Stat,getattr(Unit,self.Stat) * self.Value)