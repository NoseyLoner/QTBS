from Constants import Constants
from random import choice,randint
from typing import Callable
from Observers import PlayerClass,GameClass
from StatusEffects import *
import rich

Player = PlayerClass(Constants.Friendly)

class Singleton(type):
    
    Instances = {}

    def __call__(cls,*args,**kwargs):
        if cls not in cls.Instances:
            cls.Instances[cls] = super().__call__(*args,**kwargs)
        return cls.Instances[cls]

class ShopClass(metaclass = Singleton):

    RarityChances:dict[Constants,int] = {Constants.Legendary:7,Constants.Epic:25,Constants.Rare:55,Constants.Common:100}
    Rarities:list[Constants] = [Constants.Common]
    Size:int = 2
    # ?
    Basket:list['Upgrades'] = []

    def __init__(self):
        self.Shelf = self.Stock()
        
    def Rescale(self):
        ScaledRarityChances:dict[Constants,int] = {}
        Total:int = sum([self.RarityChances[Rarity] for Rarity in self.Rarities])
        for Rarity in self.Rarities:
            ScaledRarityChances[Rarity] = round((self.RarityChances[Rarity] / Total) * 100)
        if sum(ScaledRarityChances.values()) != 100:
            Difference = 100 - sum(ScaledRarityChances.values())
            ScaledRarityChances[Constants.Common] += Difference
        return ScaledRarityChances

    def Stock(self,Restock = False): #Hmmm?
        if Restock:
            self.Shelf.clear()
        Inventory:dict[str,list[Upgrades]] = {"Upgrades":[],"Shop Upgrades":[]}
        if self.Rarities == [Constants.Legendary,Constants.Epic,Constants.Rare,Constants.Common]:
            CurrentRarityChances = self.RarityChances
        else:
            CurrentRarityChances = self.Rescale()
        for i in range(self.Size):
            Roll = randint(1,100)
            for IRarity in self.Rarities:
                if Roll <= CurrentRarityChances[IRarity]:
                    Inventory["Upgrades"].append(Upgrades(Rarity = IRarity))
                    break
        if self.Size < 5:
            Inventory["Shop Upgrades"].append(Upgrades(Size = self.Size + 1)) # Ummmm
        if len(self.Rarities) < 4:
            NextRarity:Constants = list(self.RarityChances.keys())[3 - len(self.Rarities)]
            Inventory["Shop Upgrades"].append(Upgrades(SRarity = NextRarity))
        return Inventory

    def Display(self,Coins:int):
        rich.print("[underline italic]Welcome to the Shop!(No Refunds)[/underline italic]")
        print(f"You have {Coins} Coins")
        if len(self.Shelf["Upgrades"]) > 0:
            rich.print("[underline]Upgrades:[/underline]")
            for Index, Item in enumerate(self.Shelf["Upgrades"], start = 1):
                print(f"U{Index}. {Item}")
                print(f"Price:{Item.Price} Coins")
        else:
            rich.print("[italic]All Upgrades Purchased[/italic]")
        if len(self.Shelf["Shop Upgrades"]) > 0:
            rich.print("\n[underline]Shop Upgrades:[/underline]")
            for Index, Item in enumerate(self.Shelf["Shop Upgrades"], start = 1):
                rich.print(f"S{Index}. {Item}")
                print(f"Price:{Item.Price} Coins")
        else:
            rich.print("[italic]All Shop Upgrades Purchased[/italic]")

    def Purchase(self,Choice:str,Customer:PlayerClass):
        if Choice[0] == "E":
            raise KeyboardInterrupt("Thanks for visiting the shop! See you soon!")
        elif Choice[0] == "U":
            if self.Shelf["Upgrades"][Choice[1] - 1].Price > Customer.Coins:
                raise ValueError(f"You don't have enough coins to purchase upgrade {Choice}!\nPlease choose a different upgrade or press 'E' to exit the shop.")
            else:
                Customer.Coins -= self.Shelf["Upgrades"][Choice[1] - 1]
                Customer.Basket.append(self.Shelf["Upgrades"].pop(Choice[1] - 1))
        elif Choice[0] == "S":
            if self.Shelf["Shop Upgrades"][Choice[1] - 1].Price > Customer.Coins:
                raise ValueError(f"You don't have enough coins to purchase shop upgrade {Choice}!\nPlease choose a different upgrade or press 'E' to exit the shop.")
            else:
                Customer.Coins -= self.Shelf["Shop Upgrades"][Choice[1] - 1]
                Customer.Basket.append(self.Shelf["Shop Upgrades"].pop(Choice[1] - 1))

    def Enter(self):
        Shop = ShopClass()
        while True:
            Tools.Clear()
            Shop.Display()
            try:
                ItemID = input("Enter the ID of the item you wish to buy (e.g. U1,S2) or press 'E' to exit.\n> ").capitalize()
                if ItemID[0] not in ["U","S","E"] or ItemID[1] not in range(1,len(Shop.Shelf["Upgrades"]) + 1) or ItemID not in range(1,len(Shop.Shelf["ShopUpgrades"])):
                    raise ValueError("Invalid Item ID! Please try again or press 'E' to exit")
                else:
                    try:
                        Shop.Purchase(ItemID,Player)
                    except ValueError as Declined:
                        print(Declined)
                        continue
                    except KeyboardInterrupt as Exit:
                        print(Exit)
                        Tools.Pause(Message = "Enter any key to exit the shop: ")
                        Tools.Wait(StartingMessage = "Exiting Shop...")
                        break
            except ValueError as Invalid:
                print(Invalid)

class Upgrades:

    PossibleUpgrades:dict[Constants,list[str]] = {
        Constants.Common:["Damage","Health"],
        Constants.Rare:["Damage","MaxHealth","Heal","Armour","Health","Chance"],
        Constants.Epic:["Damage","MaxHealth","Heal","Armour","Health","Chance","AddApplies","LevelEffects","PartyIncrease"],
        Constants.Legendary:["Damage","MaxHealth","Heal","Armour","LevelEffects","Multistack","EffectSlots","PartyIncrease"]}

    Prices:dict[str,dict[Constants | int,int]] = {
        "Damage":{Constants.Common:2,Constants.Rare:4,Constants.Epic:7,Constants.Legendary:10},
        "MaxHealth":{Constants.Rare:5,Constants.Epic:8,Constants.Legendary:11},
        "Heal":{Constants.Rare:5,Constants.Epic:7,Constants.Legendary:9},
        "Armour":{Constants.Rare:4,Constants.Epic:7,Constants.Legendary:11},
        "Health":{Constants.Common:3,Constants.Rare:6,Constants.Epic:9},
        "Chance":{Constants.Rare:4,Constants.Epic:6},
        "AddApplies":{Constants.Epic:8},
        "LevelEffects":{Constants.Epic:7,Constants.Legendary:10},
        "EffectSlots":{Constants.Legendary:12},
        "Multistack":{Constants.Legendary:12},
        "PartyIncrease":{Constants.Epic:10,Constants.Legendary:15},
        "Size":{3:10,4:15,5:20},
        "SRarity":{Constants.Rare:10,Constants.Epic:15,Constants.Legendary:20}}

    ArithmeticUpgrades:dict[str,dict[Constants,dict[str,list[int | float] | float | Constants]]] = {
        "Damage":{Constants.Common:{"Values":[2,3],"Type":Constants.Additive},
                   Constants.Rare:{"Values":[4,5],"Type":Constants.Additive},
                   Constants.Epic:{"Values":[6,7],"Type":Constants.Additive},
                   Constants.Legendary:{"Values":1.50,"Type":Constants.Multiplicative}},
        "MaxHealth":{Constants.Common:{"Values":[4,5],"Type":Constants.Additive},
                     Constants.Rare:{"Values":[6,7],"Type":Constants.Additive},
                     Constants.Epic:{"Values":[9,10],"Type":Constants.Additive},
                     Constants.Legendary:{"Values":[1.30,1.40,1.50],"Type":Constants.Multiplicative}},
        "Heal":{Constants.Rare:{"values":[2,3],"Type":Constants.Additive},
                Constants.Epic:{"values":[4,5],"Type":Constants.Additive},
                Constants.Legendary:{"values":1.50,"Type":Constants.Multiplicative}},
        "Armour":{Constants.Rare:{"Values":1.10,"Type":Constants.Multiplicative},
                  Constants.Epic:{"Values":1.15,"Type":Constants.Multiplicative},
                  Constants.Legendary:{"Values":1.20,"Type":Constants.Multiplicative}},
        "Health":{Constants.Common:{"Values":0.15,"Type":Constants.Multiplicative},
                  Constants.Rare:{"Values":0.20,"Type":Constants.Multiplicative},
                  Constants.Epic:{"Values":0.25,"Type":Constants.Multiplicative}},
        "Chance":{Constants.Rare:{"Values":1.20,"Type":Constants.Multiplicative},
                  Constants.Epic:{"Values":1.30,"Type":Constants.Multiplicative}}}

    def __init__(self,Rarity:Constants | None = None,Size:int | None = None,SRarity:Constants | None = None):
        if Rarity is not None:
            self.Rarity = Rarity
            self.Effect = choice(self.PossibleUpgrades[Rarity])
            if self.Effect in self.ArithmeticUpgrades.keys():
                self.Value = choice(list(Upgrades.ArithmeticUpgrades[self.Effect][self.Rarity]["Values"]))
            else:
                if self.Effect in ["AddApplies","LevelEffects"]:
                    self.Value:StatusEffect | int = Upgrades.Evaluate(self.Effect)
        elif Size is not None:
            self.Effect = "Size"
            self.Rarity = Size
        elif SRarity is not None:
            self.Rarity = SRarity
            self.Effect = "SRarity"
        self.Price = Upgrades.Prices[self.Effect][self.Rarity]

    def __str__(self):
        if self.Effect in Upgrades.ArithmeticUpgrades.keys():
            if Upgrades.ArithmeticUpgrades[self.Effect][self.Rarity]["Type"] == Constants.Additive:
                return f"Increases {self.Effect} by {self.Value}"
            elif Upgrades.ArithmeticUpgrades[self.Effect][self.Rarity]["Type"] == Constants.Multiplicative:
                if self.Effect == "Health":
                    return f"Increases Health by {self.Value * 100}% of Max Health"
                return f"Increases {self.Effect} by {self.Value * 100 - 100}%"
        elif self.Effect == "AddApplies":
            return f"Lets a unit apply the {self.Value.Name} Status Effect"
        elif self.Effect == "LevelEffects":
            return f"Increases the level of a Status Effect by {self.Value}"
        elif self.Effect == "Multistack":
            return f"Lets a unit stack multiple Status Effects at once"
        elif self.Effect == "EffectSlots":
            return f"Increases the number of Status Effect Slots by 1"
        elif self.Effect == "PartyIncrease":
            return f"Increases the party size by 1"
        elif self.Effect == "Size":
            return f"Increases the size of the shop by 1 (max of 5)"
        elif self.Effect == "SRarity":
            return f"Allows the shop to sell {self.Rarity.value} upgrades."

    def __len__(self):
        return len(str(self))

    # What?
    # I need to do something about the arguments, how would I pass in the right consumer without having to double check the type?
    def __call__(self,Consumer:PlayerClass | ShopClass,SEName:str | None = None):
        match Consumer:
            case PlayerClass():
                if self.Effect == "PartyIncrease":
                    Consumer.Party += self.Value # Hmmmm!
            case ShopClass():
                if self.Effect == "Size":
                    Consumer.Size += 1
                elif self.Effect == "SRarity":
                    Consumer.Rarities.append(self.Rarity)
            case _:
                if self.Effect in Upgrades.ArithmeticUpgrades.keys():
                    if Upgrades.ArithmeticUpgrades[self.Effect][self.Rarity]["Type"] == Constants.Additive:
                        setattr(Consumer,self.Stat,getattr(Consumer,self.Stat) + self.Value)
                    elif Upgrades.ArithmeticUpgrades[self.Effect][self.Rarity]["Type"] == Constants.Multiplicative:
                        if self.Effect == "Health":
                            if getattr(Consumer,"Health") == getattr(Consumer,"MaxHealth"):
                                raise ValueError(f"Unit {Consumer.ID} is already at max health!")
                            setattr(Consumer,"Health",getattr(Consumer,"Health") + int(getattr(Consumer,"MaxHealth") * self.Value))
                    else:
                        setattr(Consumer,self.Stat,getattr(Consumer,self.Stat) * self.Value)
                elif self.Effect == "AddApplies":
                    self.Value.Applicate(Consumer)
                elif self.Effect == "LevelEffects":
                    TD:dict[str,StatusEffect] = {"Burning":Burning,"Weakened":Weakened,"Shocked":Shocked,"Targeted":Targeted,"Healing":Healing,"Armoured":Armoured,"Frenzied":Frenzied}
                    if Consumer.Applies[TD[SEName].Sign][TD[SEName]] == 3:
                        raise ValueError(f"{TD[SEName].Name} is already at max level!")
                    elif Consumer.Applies[TD[SEName].Sign][TD[SEName]] + self.Value > 3:
                        Consumer.Applies[TD[SEName].Sign][TD[SEName]] = 3
                    else:
                        Consumer.Applies[TD[SEName].Sign][TD[SEName]] += self.Value
                elif self.Effect == "Multistack":
                    Consumer.Multistack = True
                elif self.Effect == "EffectSlots":
                    Consumer.Slots += 1

    def Evaluate(self,Evaluatee:str):
        if Evaluatee == "AddApplies":
            return choice([Burning,Weakened,Shocked,Targeted,Healing,Armoured,Frenzied])
        elif Evaluatee == "LevelEffects":
            if self.Rarity == Constants.Epic:
                return 1
            elif self.Rarity == Constants.Legendary:
                return 2