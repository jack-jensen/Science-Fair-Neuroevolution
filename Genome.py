import random
from activations import activationFunctions as af


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
            self.gater = -1
        

    def __init__(self, identificationNumber, parent1, parent2):
        #Create the node array
        self.identificationNumber = identificationNumber
        self.parents = [parent1, parent2]
        self.initialIndex = 0
        self.numberOfInputs = 5 #Random number
        self.numberOfOutputs = 5 #Random number
        self.initialNumberOfConnections = 10 #Random number
        self.nodes = []
        self.connections = []
        self.listOfActivationFunctions = [af.binaryStep, af.linear, af.sigmoid, af.tanh,
                                af.relu, af.softsign, af.gaussian, af.sinusoid,
                               af.bentIdentity, af.bipolarStep, af.hardTanh,
                               af.selu]

        #Initiate the input and output nodes
        for i in range(self.numberOfInputs):
            self.nodes.append(self.Node("input", self.indexCalculator()))
        for i in range(self.numberOfOutputs):
            self.nodes.append(self.Node("output", self.indexCalculator()))

        self.size = len(self.nodes)

        #Initiate the connections - Making sure to mark self-connections
        for i in range(self.initialNumberOfConnections):
            pairs = []
            for node1 in self.nodes:
                for node2 in self.nodes:
                    if node1.isNotConnectedTo(node2):
                        pairs.append([node1, node2])

            pair = random.choice(pairs)

            self.connections[i] = self.Connection(pair[0], pair[1])
            

            if self.connections[i].fromIndex == self.connections[i].toIndex:
                self.connections[i].selfConnection = True





    def evaluateGenome(self, initialInputs, iterationsAllowed, waitTime):
        self.nodes.sort(key=lambda item:item.index)
        output = []
        
        for node in self.nodes:
            if node.type == "input":
                node.activation = initialInputs[node.index]
            else:
                #Check bias stuff later - it looks fishy
                for connection in self.connections:
                    if connection.toIndex == node.index:
                        if connection.selfConnection:
                            node.state += connection.weight * node.state * self.nodes[connection.gater].activation + node.bias
                        else:
                            node.state += connection.weight * self.nodes[connection.fromIndex].activation * self.nodes[connection.gater].activation
                            
                node.activation = node.activationFunction(node.state)

                if node.type == "output":
                    output.append(node)

        return output
        

    def indexCalculator(self):
        newIndex = self.initialIndex
        self.initialIndex += 1
        return newIndex
    
    def findIncomingConnections(self, node):
        incomingConnections = []
        for connection in self.connections:
            if connection.toIndex == node.index:
                incomingConnections.append(connection)

        return incomingConnections
    
    def findOutgoingConnections(self, node):
        outgoingConnections = []
        for connection in self.connections:
            if connection.fromIndex == node.index:
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


        

