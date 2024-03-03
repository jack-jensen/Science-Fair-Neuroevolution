# One of the more important files, this controls the actual generation class. It contains functions
# that are used to control the generation

import random
from Genome import serializeGenomes, Genome
from Mutations import Mutations as M
from Motor import stepper1, stepper2, stepper3, stepper4
from Activations import randomFunction
import utime

class generationRunner:
    def __init__(self, numberOfGenomes, percentageToDrop, mutationRate, genomes):
        # The variables are initiated with the parameters.
        self.listOfMutations = [M.addNodeMutation, M.addConnectionMutation, M.addGateMutation,
                           M.modifyWeightMutation,M.modifyBiasMutation, M.modifyActivationFunctionMutation,
                           M.removeNodeMutation, M.removeConnectionMutation, M.removeGateMutation]
        self.percentageToDrop = percentageToDrop
        self.mutationRate = mutationRate
        self.numberOfGenomes = numberOfGenomes
        self.newGenomes = []
        self.genomes = genomes
        print(self.genomes)
        
        # If the generation wasn't supplied with any genomes, then that probably means that
        # this is the first generation, so it has to initialze the genomes first.
        if self.genomes == []:
            # Creates as many genomes as needed
            for i in range(self.numberOfGenomes):
                
                # Initializes genome
                self.genomes.append(Genome(i, 0, ["Jack Jensen", "Jack Jensen"], [], []))
                
                # Initializes input and output nodes for the genome
                for j in range(4):
                    self.genomes[i].nodes.append(Genome.Node("input", 0, random.uniform(-5, 5), randomFunction()))
                for j in range(4):
                    self.genomes[i].nodes.append(Genome.Node("output", 0, random.uniform(-5, 5), randomFunction()))

                for node in self.genomes[i].nodes:
                    node.nodeIndex = self.genomes[i].indexCalculator()
                
                # Initializeds connections for the genome
                for node1 in self.genomes[i].nodes:
                    if node1.type == "input":
                        for node2 in self.genomes[i].nodes:
                            if node2.type == "output":
                                self.genomes[i].connections.append(Genome.Connection(node1.nodeIndex, node2.nodeIndex, False, random.uniform(-2, 2), -1))
                                
                self.genomes[i].nodes.sort(key=lambda item:item.nodeIndex)

        # Sorts genomes by identification number
        self.genomes.sort(key=lambda item:item.identificationNumber)

    # Finds the next genome to run by finding one without a fitness score.
    def findNextGenome(self):
        for genome in self.genomes:
            if genome.fitness == None:
                return genome
        return None
    
    # Runs one genome for a specified number of iterations.
    def runOneGenome(self, genome, iterations):
        outputData = []
        for i in range(iterations):
            # The inputs for the neural network are the positions of the motors
            inputs = [stepper1.position, stepper2.position, stepper3.position, stepper4.position]
            # Gets ouputs from neural net
            outputs = genome.runGenome(inputs)
            # Stores output data for later
            outputData.append(outputs)
            
            # Keeps the motor speeds slow
            stepper1.set_speed(100)
            stepper2.set_speed(100)
            stepper3.set_speed(100)
            stepper4.set_speed(100)
            
            # Runs each motor individually based on the output- making sure there is a pause in-between.
            stepper1.move_to(round(abs(outputs[0]) % 200))
            utime.sleep_ms(500)
            
            stepper2.move_to(round(abs(outputs[1]) % 200))
            utime.sleep_ms(500)
            
            stepper3.move_to(round(abs(outputs[2]) % 200))
            utime.sleep_ms(500)
            
            
            stepper4.move_to(round(abs(outputs[3]) % 200))
            utime.sleep_ms(500)
        
        # Resets the motor positions for the next motor
        stepper1.move_to(0)
        stepper2.move_to(0)
        stepper3.move_to(0)
        stepper4.move_to(0)
        
        return outputData
    
    # After all the genomes have been ran and have their fitness score, this method runs.
    def afterGenomesRan(self):
        # Sorts genomes based on fitness score
        self.genomes.sort(key=lambda item:item.fitness)
        self.rankedGenomes = self.genomes
        
        # Stores data for later
        self.serializedGenerationData = serializeGenomes(self.rankedGenomes)
        
        # Finds the number of genomes to eliminate. For example, if there were 100 genomes
        # and the percentageToDrop was 50%, you would eliminate 50 genomes.
        numberToEliminate = round(self.numberOfGenomes / self.percentageToDrop)
        for i in range(numberToEliminate):
            self.rankedGenomes.pop()
        
        # This giant while loop creates the new genomes
        while len(self.newGenomes) < self.numberOfGenomes:
            #This is how the parents are cross-breed
            # First, the parents are randomly selected
            parent1 = None
            parent2 = None
            while parent1 == parent2:
                
                parent1 = random.choice(self.rankedGenomes)
                parent2 = random.choice(self.rankedGenomes)
                
            # Second, the generationNumber of the offspring is calculated
            generationNumber = parent1.generationNumber + 1
            
            # Third, the offspring is initiated.
            offspring = Genome(len(self.newGenomes), generationNumber, [[parent1.identificationNumber, parent1.generationNumber], [parent2.identificationNumber, parent2.generationNumber]], [], [])

            # Forth, the number of nodes and connections are determined.
            # The stronger parent's size is passed down.
            if parent1.fitness > parent2.fitness:
                offspring.nodeSize = len(parent1.nodes)
                offspring.connectionSize = len(parent1.connections)

            elif parent2.fitness > parent1.fitness:
                offspring.nodeSize = len(parent2.nodes)
                offspring.connectionSize = len(parent2.connections)

            else:
                parentsList = [parent1, parent2]
                offspring.nodeSize = len(random.choice(parentsList).nodes)
                offspring.connectionSize = len(random.choice(parentsList).connections)
            
            # This adds nodes to the offspring. The nodes are selected from the parents
            i = 0
            while i < offspring.nodeSize:
                if i < offspring.nodeSize - 4:
                    if i >= len(parent1.nodes) - 4:
                        node = parent2.nodes[i]
        
                    elif i >= len(parent2.nodes) - 4: 
                        node = parent1.nodes[i]

                    else:
                        choices = [parent1.nodes[i], parent2.nodes[i]]
                        node = random.choice(choices)

                else:
                    choices = [parent1.nodes[len(parent1.nodes) + i - offspring.nodeSize],
                               parent2.nodes[len(parent2.nodes) + i - offspring.nodeSize]]
                    node = random.choice(choices)

                offspring.nodes.append(node)

                i += 1

            offspring.nodes.sort(key=lambda item:item.nodeIndex)
            
            # Same with connections.
            i = 0
            while i < offspring.connectionSize:
                
                if i > len(parent1.connections):
                    connection = parent2.connections[i]

                elif i > len(parent2.connections):
                    connection = parent1.connections[i]

                else:
                    choices = [parent1.connections[i], parent2.connections[i]]
                    connection = random.choice(choices)

                offspring.connections.append(connection)
                
                i += 1

            # Then, the offspring has the chance of getting a mutation. The act of adding a
            # mutation adds new ideas to the topology of the neural net.
            number = random.randint(0, 100)
            if number < self.mutationRate:
                # Randomly selects mutation function
                mutation = random.choice(self.listOfMutations)
                mutation(offspring)
                
            self.newGenomes.append(offspring)
        
        # Once all the new genomes are initialized, it saves a serialized copy for later.
        self.serializedGenomes = serializeGenomes(self.newGenomes)

        # In the end, it returns the new genomes, and the two pieces of data.
        return self.newGenomes, self.serializedGenomes, self.serializedGenerationData