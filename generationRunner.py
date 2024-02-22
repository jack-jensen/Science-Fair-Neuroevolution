
import random
from Genome import Genome
from Mutations import Mutations as M
import pickle
from Motor import stepper1, stepper2, stepper3, stepper4


#After each indivitaul run is complete, ask if they need to pause

# Note from first cited source: Eliminate the least successful genomes
# then cross-breed until population restored. If no progress is made
# in a certain number of generations. Then only let the top two genomes
# cross-breed

class generationRunner:
    def __init__(self, genome, numberOfGenomes, percentageToDrop, mutationRate, genomes, firstTime=False):
        self.listOfMutations = [M.addNodeMutation, M.addConnectionMutation, M.addGateMutation,
                           M.modifyWeightMutation,M.modifyBiasMutation, M.modifyActivationFunctionMutation,
                           M.removeNodeMutation, M.removeConnectionMutation, M.removeGateMutation]
        
        

        self.percentageToDrop = percentageToDrop
        self.mutationRate = mutationRate
        self.numberOfGenomes = numberOfGenomes
        self.oldGenomes = genomes
        self.genomeClass = genome
        self.firstTime = firstTime

        self.newGenomes = []
        self.genomes = []
        

        if self.firstTime:
            for i in range(self.numberOfGenomes):
                self.genomes.append(self.genomeClass(i, "Jack Jensen", "Jack Jensen"))
        else:
            if len(self.genomes) != self.numberOfGenomes:
                raise RuntimeError("Number of genomes provided does not match number of genomes needed")
            else:
                for i in range(self.numberOfGenomes):
                    self.genomes[i] = self.oldGenomes[i]
        
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
            
            stepper1.set_speed(200)
            stepper2.set_speed(200)
            stepper3.set_speed(200)
            stepper4.set_speed(200)

            stepper1.move_to(round(abs(outputs[0]) % 200))
            print(stepper1.position)
            stepper2.move_to(round(abs(outputs[1]) % 200))
            print(stepper2.position)
            stepper3.move_to(round(abs(outputs[2]) % 200))
            print(stepper3.position)
            stepper4.move_to(round(abs(outputs[3]) % 200))
            print(stepper4.position)

        stepper1.move_to(0)
        stepper2.move_to(0)
        stepper3.move_to(0)
        stepper4.move_to(0)

        

        return outputData


        
    
    def afterGenomesRan(self):
        

        self.genomes.sort(key=lambda item:item.fitness)
        self.rankedGenomes = self.genomes

        self.pickledGenerationData = pickle.dumps(self.rankedGenomes)


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

            offspring = Genome(len(self.newGenomes), parent1, parent2)
            
            
            if parent1.fitness > parent2.fitness:
                offspring.nodeSize = len(parent1.nodes)
                offspring.connectionSize = len(parent1.connections)

            elif parent2.fitness > parent1.fitness:
                offspring.nodeSize = len(parent2.nodes)
                offspring.connectionSize = len(parent2.connections)

            else:
                parentsList = [parent1, parent2]
                offspring.nodeSize = len(random.choice(parentsList).nodes)
                offspring.nodeSize = len(random.choice(parentsList).connections)


            i = 0
            while i < offspring.nodeSize:
                # Make output nodeSize  and connectionSize variable in genome class WRONG WRONG WRONG use .len()
                if i < offspring.nodeSize - 4:
                    if i > len(parent1.nodes) - 4:
                        node = parent2.nodes[i]
                    
                    elif i > len(parent2.nodes) - 4:
                        node = parent1.nodes[i]

                    else:
                        choices = [parent1.nodes[i], parent2.nodes[i]]
                        node = random.choice(choices)

                else:
                    choices = [parent1.nodes[len(parent1.nodes) + i - offspring.nodeSize],
                               parent2.nodes[len(parent2.nodes) + i - offspring.nodeSize]]
                    node = random.choice(choices)

                offspring.nodes[i] = node

                i += 1


            i = 0
            while i < offspring.connectionSize:
                if i > len(parent1.connections):
                    connection = parent2.connections[i]

                elif i > len(parent2.connections):
                    connection = parent1.connections[i]

                else:
                    choices = [parent1.connections[i], parent2.connections[i]]
                    connection = random.choice(choices)

                offspring.connections[i] = connection

            
            #Sprinkle mutations
            number = random.randint(0, 100)

            if number < self.mutationRate:
                mutation = random.choice(self.listOfMutations)
                mutation(offspring)
                
            
                
            self.newGenomes.append(offspring)
                

        #Once everything is done, this is what the class outputs
        return self.newGenomes, self.pickledGenerationData


