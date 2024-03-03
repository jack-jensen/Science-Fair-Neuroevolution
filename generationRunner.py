import random
from Genome import deserializeGenomeJSON, serializeGenomes, Genome
from Mutations import Mutations as M
from Motor import stepper1, stepper2, stepper3, stepper4
from Activations import randomFunction
import utime

#After each indivitaul run is complete, ask if they need to pause

# Note from first cited source: Eliminate the least successful genomes
# then cross-breed until population restored. If no progress is made
# in a certain number of generations. Then only let the top two genomes
# cross-breed

class generationRunner:
    def __init__(self, genomeClass, numberOfGenomes, percentageToDrop, mutationRate, genomes):
        self.listOfMutations = [M.addNodeMutation, M.addConnectionMutation, M.addGateMutation,
                           M.modifyWeightMutation,M.modifyBiasMutation, M.modifyActivationFunctionMutation,
                           M.removeNodeMutation, M.removeConnectionMutation, M.removeGateMutation]
        
        

        self.percentageToDrop = percentageToDrop
        self.mutationRate = mutationRate
        self.numberOfGenomes = numberOfGenomes
        self.oldGenomes = genomes
        self.genomeClass = genomeClass


        self.newGenomes = []
        self.genomes = []
        

        if self.genomes == []:
            for i in range(self.numberOfGenomes):
                
                self.genomes.append(self.genomeClass(i, 0, ["Jack Jensen", "Jack Jensen"], [], []))
                

                #Initiate the input and output nodes
                for j in range(4):
                    self.genomes[i].nodes.append(self.genomeClass.Node("input", 0, random.uniform(-5, 5), randomFunction()))
                for j in range(4):
                    self.genomes[i].nodes.append(self.genomeClass.Node("output", 0, random.uniform(-5, 5), randomFunction()))

                for node in self.genomes[i].nodes:
                    node.nodeIndex = self.genomes[i].indexCalculator()
                

                for node1 in self.genomes[i].nodes:
                    if node1.type == "input":
                        for node2 in self.genomes[i].nodes:
                            if node2.type == "output":
                                self.genomes[i].connections.append(self.genomeClass.Connection(node1.nodeIndex, node2.nodeIndex, False, random.uniform(-2, 2), -1))
                                
                
                
                    
                self.genomes[i].nodes.sort(key=lambda item:item.nodeIndex)

        
        self.genomes.sort(key=lambda item:item.identificationNumber)

    def findNextGenome(self):
        for genome in self.genomes:
            if genome.fitness == None:
                return genome
        return None
    
    
    def runOneGenome(self, genome, iterations):
        outputData = []
        for i in range(iterations):
            inputs = [stepper1.position, stepper2.position, stepper3.position, stepper4.position]
            outputs = genome.runGenome(inputs)
            outputData.append(outputs)
            
            stepper1.set_speed(100)
            stepper2.set_speed(100)
            stepper3.set_speed(100)
            stepper4.set_speed(100)

            stepper1.move_to(round(abs(outputs[0]) % 200))
            utime.sleep_ms(500)
            
            stepper2.move_to(round(abs(outputs[1]) % 200))
            utime.sleep_ms(500)
            
            stepper3.move_to(round(abs(outputs[2]) % 200))
            utime.sleep_ms(500)
            
            
            stepper4.move_to(round(abs(outputs[3]) % 200))
            utime.sleep_ms(500)
            

        stepper1.move_to(0)
        stepper2.move_to(0)
        stepper3.move_to(0)
        stepper4.move_to(0)

        

        return outputData


        
    
    def afterGenomesRan(self):
        
        
        self.genomes.sort(key=lambda item:item.fitness)
        self.rankedGenomes = self.genomes
        
        
        self.serializedGenerationData = serializeGenomes(self.rankedGenomes)
        
        
        
       

        numberToEliminate = round(self.numberOfGenomes / self.percentageToDrop)

        for i in range(numberToEliminate):
            self.rankedGenomes.pop()
            
      

        #Cross-breeding
        while len(self.newGenomes) < self.numberOfGenomes:
           

            parent1 = None
            parent2 = None
            while parent1 == parent2:
                
                parent1 = random.choice(self.rankedGenomes)
                parent2 = random.choice(self.rankedGenomes)
            
            generationNumber = parent1.generationNumber + 1
            offspring = Genome(len(self.newGenomes), generationNumber, [[parent1.identificationNumber, parent1.generationNumber], [parent2.identificationNumber, parent2.generationNumber]], [], [])
            
            
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


            i = 0
            while i < offspring.nodeSize:
              
                # Use len() to get the length of nodes
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

            
            #Sprinkle mutations
            number = random.randint(0, 100)

            if number < self.mutationRate:
                mutation = random.choice(self.listOfMutations)
                mutation(offspring)
                
        
                
            
                
            self.newGenomes.append(offspring)
            
      
        
        
        self.serializedGenomes = serializeGenomes(self.newGenomes)
        
        
        
      
        
        #Once everything is done, this is what the class outputs
        return self.newGenomes, self.serializedGenomes, self.serializedGenerationData


