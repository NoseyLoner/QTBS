from Constants import Constants
from typing import Any
from shutil import get_terminal_size
import rich

class Multiton(type):

    Instances = {}

    def __call__(cls,Key,*args,**kwargs):
        if Key not in cls.Instances:
            cls.Instances[Key] = super().__call__(Key,*args,**kwargs)
        return cls.Instances[Key]

# WIP!!!
class Observer:

    Messages:Any = None

    def Display(self,State:Constants,Team:Constants):
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

    def Update(self,Event:Constants,PrincipalID:str,Attribute:int | bool | str,BValue:int | bool | str,AValue:int | bool | str,Cause:str = False,OtherID:list[str] = None):
        match Event:
            case Constants.Attacking:
                AttackAnnouncement:str = f"Unit {PrincipalID} was Attacked by Unit {OtherID}!"
                AttackEffect:str = f"Health: {BValue} -> {AValue}"
                self.Messages[Constants.Attacking][PrincipalID] = {"Announcement":AttackAnnouncement,"Effect":AttackEffect}
            case Constants.UnitDeath:
                DeathAnnouncement:str = f"Unit {PrincipalID} was Killed by Unit {OtherID}!"
                self.Messages[Constants.UnitDeath][PrincipalID] = {"Announcement":DeathAnnouncement}
            case Constants.Infliction:
                inflictionAnnouncement:str = f"Unit {PrincipalID} was Inflicted with {Attribute} by Unit {OtherID}!"
                self.Messages[Constants.Infliction][PrincipalID] = {"Announcement":inflictionAnnouncement}
            case Constants.Trigger:
                TriggerAnnouncement:str = f"Unit {PrincipalID} was affected by {Attribute}!"
                self.Messages[Constants.Trigger][PrincipalID] = {"Announcement":TriggerAnnouncement}
            case Constants.Clearing:
                ClearingAnnouncement:str = f"Unit {PrincipalID} has been Cleared of {Attribute}!"
                self.Messages[Constants.Clearing][PrincipalID] = {"Announcement":ClearingAnnouncement}
            case Constants.Healing:
                HealingAnnouncement:str = f"Unit {PrincipalID} was Healed by Unit {OtherID}!"
                HealingEffect:str = f"Health: {BValue} -> {AValue}"
                self.Messages[Constants.Healing][PrincipalID] = {"Announcement":HealingAnnouncement,"Effect":HealingEffect}
            case Constants.Consuming:
                ConsumptionAnnouncement:str = f"Unit {PrincipalID} has Consumed Upgrade {OtherID}!"
                ConsumptionEffect:str = f"Unit {PrincipalID} {Attribute}: {BValue} -> {AValue}"
                self.Messages[Constants.Consuming][PrincipalID] = {"Announcement":ConsumptionAnnouncement,"Effect":ConsumptionEffect}
            case _:
                raise ValueError("Unrecognised Event Type!")

    # Name bad
    def Add(self):
        pass

class PlayerClass(Observer,metaclass = Multiton):

    def __init__(self,Team:Constants):
        self.Messages:Any = None
        self.Team = Team
        self.ShopLevel:int = 1
        self.ShopSlots:int = 2
        self.Party:int = 3
        self.Coins:int = 0
        self.Basket:list = []

class EnemyClass(Observer,metaclass = Multiton):

    def __init__(self,Team:Constants):
        self.Team = Team
        self.Level = 1