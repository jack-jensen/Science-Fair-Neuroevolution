import random
from fitnessFunctions import distanceFromXGlobal, distanceFromYGlobal, differenceFromStraight
import json
from Activations import runFunction

class Genome:

    class Node:
        def __init__(self, type, index, bias, activationFunction):
            self.type = type
            self.nodeIndex = index

            self.activation = 0
            self.state = 0

            self.bias = bias # random
            self.activationFunction = activationFunction
            
        


            
    class Connection:
        def __init__(self, fromIndex, toIndex, selfConnection, weight, gater):
            self.fromIndex = fromIndex
            self.toIndex = toIndex
            self.selfConnection = selfConnection
            self.weight = weight
            self.gater = gater #-1 normally
            
        

    def __init__(self, identificationNumber, generationNumber, parents, nodes, connections):
        self.identificationNumber = identificationNumber
        self.parents = parents
        self.fitness = None
        self.nodeSize = None
        self.connectionSize = None
        self.generationNumber = generationNumber
        

        self.nodes = nodes
        self.connections = connections

        self.initialIndex = 0
        

        

        
                        


    def runGenome(self, inputs):
        self.nodes.sort(key=lambda item:item.nodeIndex)
        output = []
        
        for node in self.nodes:
            
            if node.type == "input":
                node.activation = inputs[node.nodeIndex]
                
            else:
                #Check bias stuff later - it looks fishy
                for connection in self.connections:
                    if connection.toIndex == node.nodeIndex:
                        if connection.selfConnection:
                            node.state += connection.weight * node.state * self.nodes[connection.gater].activation + node.bias
                        else:
                            node.state += connection.weight * self.nodes[connection.fromIndex].activation * self.nodes[connection.gater].activation + node.bias
                
                node.activation = runFunction(node.state, node.activationFunction)
                
                
                

                if node.type == "output":
                    output.append(node.activation)

                    
        
        
        
        
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
                if outgoingConnection.toIndex == incomingConnection.fromIndex:
                    return True
        
        return False
    
    def calculateFitness(self, x1, y1, x2, y2):
        distanceWeight = 15
        straightnessWeight = -1
        offCenterWeight = -4
        
        fitness = (distanceFromXGlobal(y1, y2) * distanceWeight) + (distanceFromYGlobal(x1, x2) * offCenterWeight) + (differenceFromStraight(x1, y1, x2, y2) * straightnessWeight)
        
        return fitness
    
    
def serializeGenomes(genomes):
    
    genomesData = []
    
    for genome in genomes:
        nodesData = []
        connectionsData = []

        for node in genome.nodes:
            nodeData = {
                'type': node.type,
                'nodeIndex': node.nodeIndex,
                'bias': node.bias,
                'activationFunction': node.activationFunction
            }

            nodesData.append(nodeData)

        for connection in genome.connections:
            connectionData = {
                'fromIndex': connection.fromIndex,
                'toIndex': connection.toIndex,
                'selfConnection': connection.selfConnection,
                'weight': connection.weight,
                'gater': connection.gater
            }

            connectionsData.append(connectionData)
 

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
    




def deserializeGenomeJSON(JSON, numberOfGenomes):

    data = json.loads(JSON)

    if len(data['genomes']) != numberOfGenomes:
        return 'IncorrectNumberOfGenomes'
    
    genomes = []
    for genome in data['genomes']:

        nodes = []
        connections = []

        for node in genome['nodes']:
            nodes.append(Genome.Node(node['type'], node['nodeIndex'], node['bias'], node['activationFunction']))

        for connection in genome['connections']:
            connections.append(Genome.Connection(connection['fromIndex'], connection['toIndex'], connection['selfConnection'], connection['weight'], connection['gater']))

        nodes.sort(key=lambda node:node.nodeIndex)

        genomes.append(Genome(genome['identificationNumber'], genome['generationNumber'], genome['parents'], nodes, connections))

    return genomes

