from Constants import Constants
from abc import ABC,ABCMeta,abstractmethod
import Main

# All code below should work up too status effects, not sure if more needs to be done
# Also, to my knowledge this is the most advanced code I have not only written, but understood
class Singleton(type):
    
    Instances = {}

    def __call__(cls,*args,**kwargs):
        if cls not in cls.Instances:
            cls.Instances[cls] = super().__call__(*args,**kwargs)
        return cls.Instances[cls]
    
class Multiton(type):

    Instances = {}

    def __call__(cls,Key,*args,**kwargs):
        if Key not in cls.Instances:
            cls.Instances[Key] = super().__call__(Key,*args,**kwargs)
        return cls.Instances[Key]
    
class Observer():

    def Display(self):
        pass

    def Update(self):
        pass

class Director(metaclass = Singleton):
    
    def __init__(self):
        self.Controllers:dict[Constants,'Controller'] = {}

    def Attach(self,Controller:'Controller'):
        self.Controllers[Controller.Team] = Controller

    def Detach(self,Controller:'Controller'):
        self.Controllers[Controller.Team] = None

    # Might change name to Notify/Distribute
    def Update(self,Team:Constants,Name:str,Message:str):
            self.Controllers[Team].Update(Name,Message)

# Might do more later on, but is probaly complete for handiling Status Effects
class Controller(Observer,metaclass = Multiton):

    def __init__(self,Team:Constants):
        self.Team = Team
        self.Messages:dict[str,list[str]] = {}

    def Display(self):
        # Read eventually to make sure this is working as intended, or at all
        # I'm losing my mind
        for i in range(len(Main.Unit.Units[self.Team])):
            print(f"\033[4mAlerts for the {self.Team.value} team:\033[0m")
            for Message in self.Messages:
                print(Message)

    # This doesn't work
    def Update(self,Unit:str,Message:str):
        if Unit not in self.Messages:
            self.Messages[Unit] = []    
        self.Messages[Unit].append(Message)