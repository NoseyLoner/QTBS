from Constants import Constants
from abc import ABC, abstractmethod

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
            cls.Instances[Key] = super().__call__(*args,**kwargs)
        return cls.Instances[Key]
    
class Observer(ABC):

    @abstractmethod
    def Display(self):
        pass

    @abstractmethod
    def Update(self):
        pass

class Director(metaclass = Singleton):
    
    def __init__(self):
        self.Controllers:dict[Constants,'Controller'] = {}

    def Attach(self,Controller:'Controller'):
        self.Controllers[Controller.Team] = Controller

    def Detach(self,Controller:'Controller'):
        self.Controllers[Controller.Team] = None

    def Update(self,Message:str,Team:Constants):
            self.Controllers[Team].Update(Message)

# Might do more later on, but is probaly complete for handiling Status Effects
class Controller(Observer,metaclass = Multiton):

    def __init__(self,Director:Director,Team:Constants):
        self.Director = Director
        self.Team = Team
        self.Messages = []

    def Display(self):
        print(f"\033[4mAlerts for the {self.Team.name} team:\033[0m")
        for Message in self.Messages:
            print(Message)

    def Update(self,Message):
        self.Messages.append(Message)