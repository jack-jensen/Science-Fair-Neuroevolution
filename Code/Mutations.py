import random
import Activations as A

class Mutations:
    
    @staticmethod
    def addNodeMutation(genome):
        connection = random.choice(genome.connections)
        gater = connection.gater

        index = min(connection.toIndex, len(genome.nodes) - 4)
        node = genome.Node("hidden", index, random.uniform(-5, 5), A.randomFunction())

        for node in genome.nodes:
            if node.nodeIndex >= index:
                incomingConnections = genome.findIncomingConnections(node)
                outgoingConnections = genome.findOutgoingConnections(node)
                for incomingConnection in incomingConnections:
                    incomingConnection.toIndex += 1
                    if connection.gater >= index:
                        connection.gater += 1
                for outgoingConnection in outgoingConnections:
                    outgoingConnection.fromIndex += 1
                    if connection.gater >= index:
                        connection.gater += 1

                node.nodeIndex += 1
                
        genome.nodes.append(node)
        genome.nodes.sort(key=lambda node:node.nodeIndex)
        genome.connections.remove(connection)
        
        newConnection1 = genome.Connection(connection.fromIndex, index, False, random.uniform(-2, 2), -1)
        newConnection2 = genome.Connection(index, connection.toIndex, False, random.uniform(-2, 2), -1)

        if gater != -1:
            newConnections = [newConnection1, newConnection2]
            random.choice(newConnections).gater = gater

        genome.connections.append(newConnection1)
        genome.connections.append(newConnection2)

    @staticmethod
    def addConnectionMutation(genome):
        pairs = []
        for node1 in genome.nodes:
            for node2 in genome.nodes:
                if not genome.areNodesConnected(node1, node2):
                    pairs.append([node1, node2])

        pair = random.choice(pairs)

        if pair[0] == pair[1]:
            selfConnection = True
        else:
            selfConnection = False

        genome.connections.append(genome.Connection(pair[0].nodeIndex, pair[1].nodeIndex, selfConnection, random.uniform(-2, 2), -1))

    @staticmethod
    def addGateMutation(genome):
        connection = random.choice(genome.connections)
        connection.gater = random.choice(genome.nodes).nodeIndex

    @staticmethod
    def modifyWeightMutation(genome, min=-1, max=1):
        connection = random.choice(genome.connections)
        modification = round(random.uniform(0, 1), 5) * (max - min) + min

        connection.weight += modification

    @staticmethod
    def modifyBiasMutation(genome, min=-1, max=1):

        nodesWithoutInputs = []
        for node in genome.nodes:
            if not node.type == "input":
                nodesWithoutInputs.append(node)

        node = random.choice(nodesWithoutInputs)
        modification = round(random.uniform(0, 1), 5) * (max - min) + min

        node.bias += modification

    @staticmethod
    def modifyActivationFunctionMutation(genome):
        node = random.choice(genome.nodes)
        newActivationFunction = A.randomFunction()

        node.activationFunction = newActivationFunction

    @staticmethod
    def removeNodeMutation(genome):
        hiddenNodes = []
        for node in genome.nodes:
            if node.type == 'hidden':
                hiddenNodes.append(node)
        
        if len(hiddenNodes) > 0:
            node = random.choice(hiddenNodes)
        else:
            return
        
        sourceNodes = []
        gaters = []

        for connection in genome.findIncomingConnections(node):
            if connection.fromIndex != node.nodeIndex:
                sourceNodes.append(genome.nodes[connection.fromIndex])
                if connection.gater != -1:
                    gaters.append(connection.gater)
        
        targetNodes = []

        for connection in genome.findOutgoingConnections(node):
            if connection.toIndex != node.nodeIndex:
                targetNodes.append(genome.nodes[connection.toIndex])
                if connection.gater != -1:
                    gaters.append(connection.gater)

        newConnections = []

        for source in sourceNodes:
            for target in targetNodes:
                if genome.areNodesConnected(source, target):
                    newConnections.append(genome.Connection(source, target))
                    genome.connections.append(connection)

        for gater in gaters:
            if len(newConnections) == 0:
                break

            randomConnection = random.choice(newConnections)

            randomConnection.gater = gater
            newConnections.remove(randomConnection)

        for connection in genome.connections:
            if connection.gater == node.nodeIndex:
                connection.gater = -1
        
        genome.nodes.remove(node)

    @staticmethod
    def removeConnectionMutation(genome):
        connections = []

        for connection in genome.connections:
            if len(genome.findOutgoingConnections(genome.nodes[connection.fromIndex])) > 1 and len(genome.findIncomingConnections(genome.nodes[connection.toIndex])) > 1:
                connections.append(connection)

        connection = random.choice(connections)
        genome.connections.remove(connection)

    @staticmethod
    def removeGateMutation(genome):
        gatedConnections = []

        for connection in genome.connections:
            if connection.gater != -1:
                gatedConnections.append(connection)
        
        if len(gatedConnections) > 0:
            connection = random.choice(gatedConnections)
            connection.gater = -1
        else:
            print("No gated connections to remove")