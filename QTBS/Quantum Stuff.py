from math import sqrt
import cmath
import fractions
import sympy


class Qubit:

    def __init__(self,Amplitudes:tuple,RP = 1):
        self.Amplitudes = Amplitudes
        self.RP = round(cmath.phase(complex(RP)),2)

    def __str__(self):
        return (f"{self.A0}|0⟩ + {self.RP} {self.A1}|1⟩")
    
    def __mul__(self,Other):
        Sum = ""
        for i in range(4):
            Sum += f"|{bin(i)[2:].zfill(2)}⟩ + "
        Sum = Sum[:-3]
        return Sum

class MQS:

    def __init__(self,Qubits):
        self.Qubits = Qubits

    def Display(self):
        States = {}
        for i in range(len(self.Qubits)):
            States[f"Qubit{i+1}"] = ...


Test = Qubit(1/sqrt(2),1/sqrt(2),"j")
Test2 = Qubit(sqrt(3)/2,1/2)
print(Test)
print(Test2)
print(Test * Test2)

