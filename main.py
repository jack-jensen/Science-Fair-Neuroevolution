#OPTIONAL: IF TIME, YOU MAY ADD GATERS TO THE CONNECTIONS
import random
import math
from activations import activationFunctions as af
import time

#Dummy code
class Pin:
    def __init__(self, pin, action):
        pass

    def OUT():
        pass

    def value(number):
        pass

    

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
            self.activation = 0
            self.state = 0
            self.bias = 0
            self.activationFunction = af.linear
            


            
    class Connection:
        def __init__(self, fromIndex, toIndex):
            self.fromIndex = fromIndex
            self.toIndex = toIndex
            self.selfConnection = False
            self.weight = 0
            

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


    
    def sortNodesKey(self, e):
        return e.index


    def evaluateGenome(self, initialInputs, iterationsAllowed, waitTime):
        self.nodes.sort(key=self.sortNodesKey)
        i = 0
        while i <= iterationsAllowed:
            for node in self.nodes:
                if node.type == "input":
                    node.activation = initialInputs[node.index]
                else:
                    #Check bias stuff later - it looks fishy
                    #Also don't forget to add the gaters later
                    #Add a wait time as to not overload the motors
                    for connection in self.connections:
                        if connection.toIndex == node.index:
                            if connection.selfConnection:
                                node.state += connection.weight * node.state + node.bias
                            else:
                                node.state += connection.weight * self.nodes[connection.fromIndex].activation
                            
                    node.activation = node.activationFunction(node.state)

                    if node.type == "output":
                        pass
                    
            i += 1

        #Get fitness - code once the dashboard is set up
        

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
