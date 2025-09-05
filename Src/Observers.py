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
            rich.print(f"{FTitle:<{Width}}{HTitle:>{Width}}")

    
    def FormatUpdate(self,State:Constants,ID:str,Attribute:int | bool | str,BValue:int | bool | str,AValue:int | bool | str,Cause:Any = False):
        FMesssage:str = f"Unit {ID}, {Attribute}: {BValue} -> {AValue}"
        self.Update(State,ID,FMesssage)
    
    def Update(self,State:Constants,ID:str,Message:str):
        self.Messages[State][ID] = Message

class PlayerClass(Observer,metaclass = Multiton):

    def __init__(self,Team:Constants):
        self.Messages:dict[Constants,dict[str,str]] = {Constants.Start:{},Constants.End:{},Constants.Shopping:{},Constants.Turn:{}}
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