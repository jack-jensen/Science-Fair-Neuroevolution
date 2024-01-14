import math
#This file was painstakenly type out by hand




class activationFunctions:

    @staticmethod
    def binaryStep(x):
        if x <= 0:
            return 0
        elif x > 0:
            return 1
        else:
            print("You screwed something up")

    @staticmethod
    def linear(x):
        return x
    
    @staticmethod
    def sigmoid(x):
        return 1 / 1 + math.exp(-x)
    
    @staticmethod
    def tanh(x):
        return (math.exp(x) - math.exp(-x)) / (math.exp(x) + math.exp(-x))
    
    @staticmethod
    def relu(x):
        if x <= 0:
            return 0
        else:
            return x
    
    @staticmethod
    def softsign(x):
        return x / 1 + abs(x)
    
    @staticmethod
    def gaussian(x):
        return math.exp(-x ** 2)
    
    @staticmethod
    def sinusoid(x):
        return math.sin(x)
    
    @staticmethod
    def bentIdentity(x):
        return ((math.sqrt((x ** 2) + 1) - 1) / 2) + x
    
    @staticmethod
    def bipolarStep(x):
        if x <= 0:
            return -1
        elif x > 0:
            return 1
        else:
            print("You screwed something up")

    @staticmethod
    def hardTanh(x):
        if x < -1:
            return -1
        elif -1 <= x <= 1:
            return x
        elif x > 1:
            return 1
        
    @staticmethod
    def selu(x):
        a = 1.6733
        y = 1.0507

        if x >= 0:
            return y * x
        elif x < 0:
            return (y * a) * (math.exp(x) - 1)
