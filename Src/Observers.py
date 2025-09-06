from Constants import Constants
from typing import Any
from shutil import get_terminal_size
import rich
from itertools import zip_longest

class Multiton(type):

    Instances = {}

    def __call__(cls,Key,*args,**kwargs):
        if Key not in cls.Instances:
            cls.Instances[Key] = super().__call__(Key,*args,**kwargs)
        return cls.Instances[Key]

# WIP!!!
class Observer:

    Messages:dict[Constants,dict[str,dict[Constants,dict[str,str]]]] = {
        Constants.Start:{},
        Constants.End:{},
        Constants.Shopping:{}}

    def Display(self,State:Constants):
        match State:
            case Constants.Start:
                if len(self.Messages[Constants.Start]) > 0:
                    Width = get_terminal_size().columns()
                    rich.print(f"[underline]Start Of Turn Updates:")
                    FTitle = f"[underline]Friendly:[/underline]"
                    HTitle = f"[underline]Hostile:[/underline]"
                    print(f"{FTitle:<{Width//2}}{HTitle}")
                    FSIDs = [FIDs for FIDs in self.Messages[Constants.Start].keys() if "F" in FIDs]
                    HSIDs = [HIDs for HIDs in self.Messages[Constants.Start].keys() if "H" in HIDs]
                    if len(FSIDs) > 0 and len(HSIDs) > 0:
                        FSUpdates = []
                        HSUpdates = []
                        for FID,HID in zip_longest(FSIDs,HSIDs):
                            if FID is not None:
                                FSUpdates.append(self.Messages[Constants.Start][FID].values())
                        print(f"Unit {FID + ":":<{Width//2}}Unit {HID}:")
                        self.Messages.get

    def BadDisplay(self,State:Constants,Team:Constants):
        if Team == Constants.Friendly:
            for ID,Message in self.Messages[State].items():
                rich.print(f"[underline]Unit {ID} Updates:[/underline]")
                print(f"    {Message}")
            self.Messages[State].clear()
        else:
            Width = get_terminal_size().columns()
            FTitle = "[underline]Friendly Team Updates:[/underline]"
            HTitle = "[underline]Hostile Team Updates:[/underline]" 
            rich.print(f"{FTitle:<{Width//2}}{HTitle}")
            ...

    def Update(self,Event:Constants,PrincipalID:str,Attribute:int | bool | str,BValue:int | bool | str,AValue:int | bool | str,OtherID:list[str] = None):
        match Event:
            case Constants.Attacking:
                AttackAnnouncement:str = f"Unit {PrincipalID} was Attacked by Unit {OtherID[0]}!"
                AttackEffect:str = f"Health: {BValue} -> {AValue}"
                self.Messages[Constants.End][PrincipalID][Constants.Attacking] = {"Announcement":AttackAnnouncement,"Effect":AttackEffect}
            case Constants.UnitDeath:
                DeathAnnouncement:str = f"Unit {PrincipalID} was Killed by Unit {OtherID[0]}!"
                self.Messages[Constants.End][PrincipalID][Constants.UnitDeath] = {"Announcement":DeathAnnouncement}
            case Constants.Infliction:
                inflictionAnnouncement:str = f"Unit {PrincipalID} was Inflicted with {Attribute} by Unit {OtherID[0]}!"
                self.Messages[Constants.End][PrincipalID][Constants.Infliction] = {"Announcement":inflictionAnnouncement}
            case Constants.Trigger:
                TriggerAnnouncement:str = f"Unit {PrincipalID} was affected by {Attribute}!"
                self.Messages[Constants.Start][PrincipalID][Constants.Trigger] = {"Announcement":TriggerAnnouncement}
            case Constants.Clearing:
                ClearingAnnouncement:str = f"Unit {PrincipalID} has been Cleared of {Attribute}!"
                self.Messages[Constants.Start][PrincipalID][Constants.Clearing] = {"Announcement":ClearingAnnouncement}
            case Constants.Healing:
                HealingAnnouncement:str = f"Unit {PrincipalID} was Healed by Unit {OtherID[0]}!"
                HealingEffect:str = f"Health: {BValue} -> {AValue}"
                self.Messages[Constants.End][PrincipalID][Constants.Healing] = {"Announcement":HealingAnnouncement,"Effect":HealingEffect}
            case Constants.Consumption:
                ConsumptionAnnouncement:str = f"Unit {PrincipalID} has Consumed Upgrade {OtherID[0]}!"
                ConsumptionEffect:str = f"Unit {PrincipalID} {Attribute}: {BValue} -> {AValue}"
                self.Messages[Constants.Shopping][PrincipalID][Constants.Consumption] = {"Announcement":ConsumptionAnnouncement,"Effect":ConsumptionEffect}
            case Constants.Blocked:
                BlockAnnouncement:str = f"Unit {PrincipalID} blocked unit {OtherID[0]}'s attack on unit {OtherID[1]}!"
                BlockEffect:str = f"Unit {PrincipalID}'s Health: {BValue} -> {AValue}"
                self.Messages[Constants.End][PrincipalID][Constants.Blocked] = {"Announcement":BlockAnnouncement,"Effect":BlockEffect}
            case _:
                raise ValueError("Unrecognised Event Type!")

class PlayerClass(metaclass = Multiton):

    def __init__(self,Team:Constants):
        self.Messages:Any = None
        self.Team = Team
        self.ShopLevel:int = 1
        self.ShopSlots:int = 2
        self.Party:int = 3
        self.Coins:int = 0
        self.Basket:list = []

class EnemyClass(metaclass = Multiton):

    def __init__(self,Team:Constants):
        self.Team = Team
        self.Level = 1