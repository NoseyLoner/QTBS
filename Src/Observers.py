from Constants import Constants
from typing import Any
from shutil import get_terminal_size
from itertools import zip_longest
import rich

class Multiton(type):

    Instances = {}

    def __call__(cls,Key,*args,**kwargs):
        if Key not in cls.Instances:
            cls.Instances[Key] = super().__call__(Key,*args,**kwargs)
        return cls.Instances[Key]

# Name is a work in progress
class Overseer:

    Messages:dict[Constants,dict[str,list[dict[str,str | Constants]]]] = {
        Constants.Start:{},
        Constants.End:{},
        Constants.Shopping:{}}

    def Display(self,State:Constants,Team:Constants):
        match State:
            case Constants.Start:
                if len(self.Messages[Constants.Start]) > 0:
                    rich.print(f"[underline]{Team} Start Of Turn Updates:[/underline]")
                    for ID in self.Messages[Constants.Start]:
                        if str(Team)[0] in ID:
                            TSIndent:int = 4 
                            print(ID)
                            for TSMessage in self.Messages[Constants.Start][ID]:
                                print(f"{' '*TSIndent}{TSMessage['Announcement']}")
                                if "Effect" in TSMessage:
                                    TSIndent += 4
                                    print(f"{' '*TSIndent}{TSMessage['Effect']}")
                                    TSIndent -= 4
                    self.Messages[Constants.Start].clear()
                else:
                    rich.print("[italic]No Start of Turn Updates.[/italic]")
            case Constants.End:
                if len(self.Messages[Constants.End]) > 0:
                    rich.print(f"[underline]{Team} End Of Turn Updates:[/underline]")
                    for ID in self.Messages[Constants.End]:
                        if str(Team)[0] in ID:
                            TSIndent:int = 4 
                            print(ID)
                            for TSMessage in self.Messages[Constants.End][ID]:
                                print(f"{' '*TSIndent}{TSMessage['Announcement']}")
                                if "Effect" in TSMessage:
                                    TSIndent += 4
                                    print(f"{' '*TSIndent}{TSMessage['Effect']}")
                                    TSIndent -= 4
                    self.Messages[Constants.End].clear()
                else:
                    rich.print("[italic]No End of Turn Updates.[/italic]")
            case Constants.Shopping:
                if len(self.Messages[Constants.Shopping]) > 0:
                    rich.print(f"[underline]{Team} Shopping Updates:[/underline]")
                    for ID in self.Messages[Constants.Shopping]:
                        if str(Team)[0] in ID:
                            TSIndent:int = 4 
                            print(ID)
                            for TSMessage in self.Messages[Constants.Shopping][ID]:
                                print(f"{' '*TSIndent}{TSMessage['Announcement']}")
                                if "Effect" in TSMessage:
                                    TSIndent += 4
                                    print(f"{' '*TSIndent}{TSMessage['Effect']}")
                                    TSIndent -= 4
                    self.Messages[Constants.Shopping].clear()
                else:
                    rich.print("[italic]No Shopping Updates.[/italic]")
            case _:
                raise ValueError("Unrecognised State Type!")

    def Update(self,Event:Constants,PrincipalID:str,Attribute:Any,BValue:Any,AValue:Any,OtherID:list[str] = None):
        match Event:
            case Constants.Attacking:
                AttackAnnouncement:str = f"Unit {PrincipalID} attacked Unit {OtherID[0]}:"
                AttackEffect:str = f"Health: {BValue} -> {AValue}"
                self.Messages[Constants.End][PrincipalID].append({"Announcement":AttackAnnouncement,"Effect":AttackEffect,"Event":Event})
            case Constants.UnitDeath:
                DeathAnnouncement:str = f"Unit {PrincipalID} has killed Unit {OtherID[0]}!"
                self.Messages[Constants.End][PrincipalID].append({"Announcement":DeathAnnouncement,"Event":Event})
            case Constants.Infliction:
                inflictionAnnouncement:str = f"Unit {PrincipalID} has inflicted Unit {OtherID[0]}! with {Attribute}"
                self.Messages[Constants.End][PrincipalID].append({"Announcement":inflictionAnnouncement,"Event":Event})
            case Constants.Trigger:
                TriggerAnnouncement:str = f"Unit {PrincipalID} was affected by {Attribute}, {Attribute.Turns} turns left"
                self.Messages[Constants.Start][PrincipalID].append({"Announcement":TriggerAnnouncement,"Event":Event})
            case Constants.Clearing:
                ClearingAnnouncement:str = f"Unit {PrincipalID} has been cleared of {Attribute}!"
                self.Messages[Constants.Start][PrincipalID].append({"Announcement":ClearingAnnouncement,"Event":Event})
            case Constants.Healing:
                HealingAnnouncement:str = f"Unit {PrincipalID} healed Unit {OtherID[0]}:"
                HealingEffect:str = f"Health: {BValue} -> {AValue}"
                self.Messages[Constants.End][PrincipalID].append({"Announcement":HealingAnnouncement,"Effect":HealingEffect,"Event":Event})
            case Constants.Consumption: # Hmmm
                ConsumptionAnnouncement:str = f"Unit {PrincipalID} has consumed Upgrade {OtherID[0]}!:"
                ConsumptionEffect:str = f"Unit {PrincipalID} {Attribute}: {BValue} -> {AValue}"
                self.Messages[Constants.Shopping][PrincipalID].append({"Announcement":ConsumptionAnnouncement,"Effect":ConsumptionEffect,"Event":Event})
            case Constants.Blocked:
                BlockAnnouncement:str = f"Unit {PrincipalID} blocked unit {OtherID[0]}'s attack on unit {OtherID[1]}!"
                BlockEffect:str = f"Unit {PrincipalID}'s Health: {BValue} -> {AValue}"
                self.Messages[Constants.End][PrincipalID].append({"Announcement":BlockAnnouncement,"Effect":BlockEffect,"Event":Event})
            case Constants.Shielding:
                ShieldAnnouncement:str = f"Unit {PrincipalID} is shielding unit {OtherID[0]}!"
                self.Messages[Constants.Start][PrincipalID].append({"Announcement":ShieldAnnouncement,"Event":Event})   
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