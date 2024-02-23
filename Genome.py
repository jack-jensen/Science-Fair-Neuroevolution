import random
from Activations import activationFunctions as af
import pickle
from fitnessFunctions import distanceFromXGlobal, distanceFromYGlobal, differenceFromStraight



class Genome:

    class Node:
        def __init__(self, type, index):
            self.listOfActivationFunctions = [af.binaryStep, af.linear, af.sigmoid, af.tanh,
                                af.relu, af.softsign, af.gaussian, af.sinusoid,
                               af.bentIdentity, af.bipolarStep, af.hardTanh,
                               af.selu]
            self.type = type
            self.nodeIndex = index
            self.activation = 0
            self.state = 0
            self.bias = random.random()
            self.activationFunction = random.choice(self.listOfActivationFunctions)


            
    class Connection:
        def __init__(self, fromIndex, toIndex, selfConnection=False):
            self.fromIndex = fromIndex
            self.toIndex = toIndex
            self.selfConnection = selfConnection
            self.weight = random.random()
            self.gater = -1
            print(self.weight)
        

    def __init__(self, identificationNumber, parent1, parent2):
        self.identificationNumber = identificationNumber
        self.parents = [parent1, parent2]
        self.initialIndex = 0
        self.numberOfInputs = 4 #The angle of the motors
        self.numberOfOutputs = 4 #The increment that the angle changes for each motor
        self.fitnessBigOutputs = 0
        self.fitness = None
        self.nodeSize = None
        self.connectionSize = None

        self.nodes = []
        self.connections = []
        

        #Initiate the input and output nodes
        for i in range(self.numberOfInputs):
            self.nodes.append(self.Node("input", self.indexCalculator()))
        for i in range(self.numberOfOutputs):
            self.nodes.append(self.Node("output", self.indexCalculator()))

        self.size = len(self.nodes)
        self.nodes.sort(key=lambda item:item.nodeIndex)

        #initiate the connections
        for node1 in self.nodes:
            if node1.type == 'input':
                for node2 in self.nodes:
                    if node2.type == "output":
                        self.connections.append(self.Connection(node1.nodeIndex, node2.nodeIndex))
                        


    def runGenome(self, inputs):
        self.nodes.sort(key=lambda item:item.nodeIndex)
        output = []
        
        for node in self.nodes:
            print(node.activationFunction)
            if node.type == "input":
                node.activation = inputs[node.nodeIndex]
                print(node.activation)
            else:
                #Check bias stuff later - it looks fishy
                for connection in self.connections:
                    if connection.toIndex == node.nodeIndex:
                        if connection.selfConnection:
                            node.state += connection.weight * node.state * self.nodes[connection.gater].activation + node.bias
                        else:
                            node.state += connection.weight * self.nodes[connection.fromIndex].activation * self.nodes[connection.gater].activation
                
                node.activation = node.activationFunction(node.state)
                print("output" + str(node.activation))
                
                

                if node.type == "output":
                    output.append(node.activation)
                    print(output)
        
        
        print(output)
        
        return output
        

    def indexCalculator(self):
        newIndex = self.initialIndex
        self.initialIndex += 1
        return newIndex
    
    def findIncomingConnections(self, node):
        incomingConnections = []
        for connection in self.connections:
            if connection.toIndex == node.nodeIndex:
                incomingConnections.append(connection)

        return incomingConnections
    
    def findOutgoingConnections(self, node):
        outgoingConnections = []
        for connection in self.connections:
            if connection.fromIndex == node.nodeIndex:
                outgoingConnections.append(connection)

        return outgoingConnections

            
    def areNodesConnected(self, node1, node2):
        """Is this more complicated than it needs to be? Probably!"""
        incomingNode1 = self.findIncomingConnections(node1)
        outgoingNode1 = self.findOutgoingConnections(node1)
        incomingNode2 = self.findIncomingConnections(node2)
        outgoingNode2 = self.findOutgoingConnections(node2)

        for incomingConnection in incomingNode1:
            for outgoingConnection in outgoingNode2:
                if incomingConnection.fromIndex == outgoingConnection.toIndex:
                    return True
        for outgoingConnection in outgoingNode1:
            for incomingConnection in incomingNode2:
                if outgoingConnection.toindex == incomingConnection.fromIndex:
                    return True
                
        return False
    
    def calculateFitness(self, x1, y1, x2, y2):
        distanceWeight = 15
        straightnessWeight = -1
        offCenterWeight = -4
        
        fitness = (distanceFromXGlobal(y1, y2) * distanceWeight) + (distanceFromYGlobal(x1, x2) * offCenterWeight) + (differenceFromStraight(x1, y1, x2, y2) * straightnessWeight)
        
        return fitness




def unPickleGenomeFile(fileName, numberOfGenomes):
    try:
        with open(fileName, "rb") as file:
            raw_lines = file.readlines()
            if len(raw_lines) < numberOfGenomes:
                return "wrongNumber"
            genomes = []
            try:
                for raw_line in raw_lines:
                    line = pickle.loads(raw_line)
                    genomes.append(line)
            except Exception as e:
                print(f"Failed to unPickle \n {e}")
                return "Error"
            genomes.sort(key=lambda genome:genome.identificationNumber)
            
        return genomes
    except Exception as e:
        print(f"Error \n {e}")
        return "Error"

