# This file holds the genome class.

from fitnessFunctions import distanceFromXGlobal, distanceFromYGlobal, differenceFromStraight
import json
from Activations import runFunction

class Genome:
    
    # I probably didn't have to nest the node and connection class, but that is what I did.
    class Node:
        def __init__(self, type, index, bias, activationFunction):
            # This initializes the variables for the nodes
            self.type = type
            self.nodeIndex = index
            self.activation = 0
            self.state = 0
            self.bias = bias
            self.activationFunction = activationFunction
            
    class Connection:
        def __init__(self, fromIndex, toIndex, selfConnection, weight, gater):
            # This initializes the variables for the connections
            self.fromIndex = fromIndex
            self.toIndex = toIndex
            self.selfConnection = selfConnection
            self.weight = weight
            self.gater = gater
            
    def __init__(self, identificationNumber, generationNumber, parents, nodes, connections):
        # This initializes the variables for the genome as a whole
        self.identificationNumber = identificationNumber
        self.parents = parents
        self.fitness = None
        self.nodeSize = None
        self.connectionSize = None
        self.generationNumber = generationNumber
        self.nodes = nodes
        self.connections = connections
        self.initialIndex = 0
    
    
    # This method contains most of the maths in this project. 
    # This actually runs through the neural network of the genome.
    def runGenome(self, inputs):
        self.nodes.sort(key=lambda item:item.nodeIndex)
        output = []
        
        for node in self.nodes:
            # If the node is an input, then the activation is the input!
            if node.type == "input":
                node.activation = inputs[node.nodeIndex]
            else:
                for connection in self.connections:
                    if connection.toIndex == node.nodeIndex:
                        
                        if connection.selfConnection:
                            # If the connection is a self connection, then multiplies the weight by the current
                            # state of the node and the activation of the gate node, plus the bias
                            node.state += connection.weight * node.state * self.nodes[connection.gater].activation + node.bias
                        else:
                            # Normally, the state of the nod is the weight multiplied by the previous node
                            # activation and the gate node, plus the bias
                            node.state += connection.weight * self.nodes[connection.fromIndex].activation * self.nodes[connection.gater].activation + node.bias
                
                # The activation is determined by the output of the activation function with
                # the node state as the input.
                node.activation = runFunction(node.state, node.activationFunction)
                
                # If the node is an output then the activation is added to the outputs.
                if node.type == "output":
                    output.append(node.activation)

        return output
    
    # Calculates the index for new nodes
    def indexCalculator(self):
        newIndex = self.initialIndex
        self.initialIndex += 1
        return newIndex
    
    # Finds incoming connections to a node
    def findIncomingConnections(self, node):
        incomingConnections = []
        for connection in self.connections:
            if connection.toIndex == node.nodeIndex:
                incomingConnections.append(connection)

        return incomingConnections
    
    # Finds outgoing connections from a node
    def findOutgoingConnections(self, node):
        outgoingConnections = []
        for connection in self.connections:
            if connection.fromIndex == node.nodeIndex:
                outgoingConnections.append(connection)

        return outgoingConnections

    # Finds if nodes connected
    def areNodesConnected(self, node1, node2):
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
                if outgoingConnection.toIndex == incomingConnection.fromIndex:
                    return True
        
        return False
    
    # Calculates the fitness from the outputs of the functions in the fitnessFunction file
    def calculateFitness(self, x1, y1, x2, y2):
        # Also has weights to indicate how important a value is
        distanceWeight = 15
        straightnessWeight = -1
        offCenterWeight = -4
        
        fitness = (distanceFromXGlobal(y1, y2) * distanceWeight) + (distanceFromYGlobal(x1, x2) * offCenterWeight) + (differenceFromStraight(x1, y1, x2, y2) * straightnessWeight)
        
        return fitness
    
    
    
    
# This function is outside the genome class and serializes the genome data for later. 
# (This function is only used in other files).
def serializeGenomes(genomes):
    
    genomesData = []
    
    for genome in genomes:
        nodesData = []
        connectionsData = []

        # Serializes nodes
        for node in genome.nodes:
            nodeData = {
                'type': node.type,
                'nodeIndex': node.nodeIndex,
                'bias': node.bias,
                'activationFunction': node.activationFunction
            }

            nodesData.append(nodeData)

        # Serializes connections
        for connection in genome.connections:
            connectionData = {
                'fromIndex': connection.fromIndex,
                'toIndex': connection.toIndex,
                'selfConnection': connection.selfConnection,
                'weight': connection.weight,
                'gater': connection.gater
            }

            connectionsData.append(connectionData)

        # Serializes genome
        genomeData = {
            'identificationNumber': genome.identificationNumber,
            'parents': genome.parents,
            'initialIndex': genome.initialIndex,
            'fitness': genome.fitness,
            'nodeSize': genome.nodeSize,
            'connectionSize': genome.connectionSize,
            'nodes': nodesData,
            'connections': connectionsData,
            'generationNumber': genome.generationNumber

        }

        genomesData.append(genomeData)

    allData = {
        'genomes': genomesData
    }

    serializedGenomes = json.dumps(allData)
    return serializedGenomes