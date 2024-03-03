import math
import random

def binaryStep(x):
    if x <= 0:
        return 0
    elif x > 0:
        return 1

def linear(x):
    return x

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def tanh(x):
    return (math.exp(x) - math.exp(-x)) / (math.exp(x) + math.exp(-x))

def relu(x):
    if x <= 0:
        return 0
    else:
        return x

def softsign(x):
    return x / (1 + abs(x))

def gaussian(x):
    return math.exp(-x ** 2)

def sinusoid(x):
    return math.sin(x)

def bentIdentity(x):
    return ((math.sqrt((x ** 2) + 1) - 1) / 2) + x

def bipolarStep(x):
    if x <= 0:
        return -1
    elif x > 0:
        return 1

def hardTanh(x):
    if x < -1:
        return -1
    elif -1 <= x <= 1:
        return x
    else:
        return 1
    
def selu(x):
    a = 1.6733
    y = 1.0507

    if x >= 0:
        return y * x
    elif x < 0:
        return (y * a) * (math.exp(x) - 1)

def randomFunction():
        return random.choice([
            "binaryStep",
            "linear",
            "sigmoid",
            "tanh",
            "relu",
            "softsign",
            "gaussian",
            "sinusoid",
            "bentIdentity",
            "bipolarStep",
            "hardTanh",
            "selu"
            ])
    
def runFunction(x, function):
    if function == "binaryStep":
        return binaryStep(x)
    elif function == "linear":
        return linear(x)
    elif function == "sigmoid":
        return sigmoid(x)
    elif function == "tanh":
        return tanh(x)
    elif function == "relu":
        return relu(x)
    elif function == "softsign":
        return softsign(x)
    elif function == "gaussian":
        return gaussian(x)
    elif function == "sinusoid":
        return sinusoid(x)
    elif function == "bentIdentity":
        return bentIdentity(x)
    elif function == "bipolarStep":
        return bipolarStep(x)
    elif function == "hardTanh":
        return hardTanh(x)
    elif function == "selu":
        return selu(x)
    else:
        print("Error in activation file")
        return "Error"