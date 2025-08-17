from Constants import Constants
    
class Multiton(type):

    Instances = {}

    def __call__(cls,Key,*args,**kwargs):
        if Key not in cls.Instances:
            cls.Instances[Key] = super().__call__(Key,*args,**kwargs)
        return cls.Instances[Key]

class Controller(metaclass = Multiton):

    def __init__(self,Team:Constants):
        self.Team = Team
        self.Coins = 0
        self.Messages:list[str] = []

    def Display(self):
        print(f"\033[4mAlerts for the {self.Team.value} team:\033[0m")
        for Message in self.Messages:
            print(Message)

    def Update(self,ID:str,Message:str):
        self.Messages.append((ID,Message))