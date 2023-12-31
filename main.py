#OPTIONAL: IF TIME, YOU MAY ADD GATERS TO THE CONNECTIONS
import random
import math
from activations import activationFunctions as af


class Pin:
    def __init__(self, pin, action):
        pass

    def OUT():
        pass

    def value(number):
        pass
#Dummy code above
    

class Motor:
    def __init__(self, firstCoil_1_p, firstCoil_2_p, secondCoil_1_p, secondCoil_2_p):
        self.firstCoil_1 = Pin(firstCoil_1_p, Pin.OUT)
        self.firstCoil_2 = Pin(firstCoil_2_p, Pin.OUT)
        self.secondCoil_1 = Pin(secondCoil_1_p, Pin.OUT)
        self.secondCoil_2 = Pin(secondCoil_2_p, Pin.OUT)

    def runClockwiseOnePhase(self):
        # blah
        # blah
        # blah
        pass
    
    def runCounterclockwiseOnePhase(self):
        # blah
        # blah
        # blah
        pass

    def stop(self):
        self.firstCoil_1.value(0)
        self.firstCoil_2.value(0)
        self.secondCoil_1.value(0)
        self.secondCoil_2.value(0)

    def runClockwiseTEST(self):
        pass

    def runCounterclockwiseTest(self):
        pass








class Genome:

    class Node:
        def __init__(self, type, index):
            self.type = type
            self.index = index


            
    class Connection:
        def __init__(self, fromIndex, toIndex):
            self.fromIndex = fromIndex
            self.toIndex = toIndex
            self.selfConnection = False
            

    def __init__(self):
        #Create the node array
        self.initialIndex = 0
        self.numberOfInputs = 5 #Random number
        self.numberOfOutputs = 5 #Random number
        self.initialNumberOfConnections = 10 #Random number
        self.nodes = []
        self.connections = []

        #Initiate the input and output nodes
        for i in range(self.numberOfInputs):
            self.nodes.append(self.Node("input", self.indexCalculator()))
        for i in range(self.numberOfOutputs):
            self.nodes.append(self.Node("output", self.indexCalculator()))

        #Initiate the connections - Making sure to mark self-connections
        for i in range(self.initialNumberOfConnections):
            self.connections.append(self.Connection(random.randint(0, self.initialIndex), random.randint(0, self.initialIndex),))
            if self.connections[i].fromIndex == self.connections[i].toIndex:
                self.connections[i].selfConnection = True


        
    def evaluateGenome():
        pass

    
        
    def indexCalculator(self):
        newIndex = self.initialIndex
        self.initialIndex += 1
        return newIndex
        

    def addNode():
        pass
    def viewNodes(self, x, y):
        print(self.nodes[y][x])
        
        
    def deleteNode():
        pass
    def addConnection():
        pass
    def viewConnections():
        pass
    def deleteConnection():
        pass


genome = Genome()
