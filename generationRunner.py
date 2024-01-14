import random
from Genome import Genome
from mutations import Mutations as M
import pickle
#After each indivitaul run is complete, ask if they need to pause

# Note from first cited source: Eliminate the least successful genomes
# then cross-breed until population restored. If no progress is made
# in a certain number of generations. Then only let the top two genomes
# cross-breed

class generationRunner:
    def __init__(self, genome, numberOfGenomes, percentageToDrop, mutationRate, genomesParameter:list, firstTime=False):
        listOfMutations = [M.addNodeMutation, M.addConnectionMutation, M.addGateMutation,
                           M.modifyWeightMutation,M.modifyBiasMutation, M.modifyActivationFunctionMutation,
                           M.removeNodeMutation, M.removeConnectionMutation, M.removeGateMutation]
        
        genomes = []
        if firstTime:
            for i in range(numberOfGenomes):
                genomes.append(genome(i, "Jack Jensen", "Jack Jensen"))
        else:
            if len(genomes) != numberOfGenomes:
                raise RuntimeError("Number of genomes provided does not match number of genomes needed")
            else:
                for i in range(numberOfGenomes):
                    genomes[i] = genomesParameter[i]



        newGenomes = []
    
        rankedGenomes = genomes.sort(key=lambda item:item.fitness)

        #Save rankedGenomes list - with all the class genome objects
        
        pickledGenerationData = pickle.dumps(rankedGenomes)


        #You may not have to eliminate the genomes. Reproduce all the genomes randomly, then the last
        # generation 'dies'.
        numberToEliminate = round(numberOfGenomes / percentageToDrop)

        for i in range(numberToEliminate):
            rankedGenomes.pop()

        #Cross-breeding
        while len(newGenomes) < numberOfGenomes:


            while parent1 != parent2:
                parent1 = random.choice(rankedGenomes)
                parent2 = random.choice(rankedGenomes)

            offspring = Genome(len(newGenomes), parent1, parent2)
            
            
            if parent1.fitness > parent2.fitness:
                offspring.nodeSize = parent1.nodeSize
                offspring.connectionSize = parent1.connectionSize

            elif parent2.fitness > parent1.fitness:
                offspring.nodeSize = parent2.nodeSize
                offspring.connectionSize = parent2.connectionSize

            else:
                #Possibly make it so that the nodeSize is between
                # the two parent's sizes instead of one or the other
                parentsList= [parent1, parent2]
                offspring.nodeSize = random.choice(parentsList).nodeSize


            i = 0
            while i < offspring.nodeSize:
                # Make output nodeSize  and connectionSize variable in genome class WRONG WRONG WRONG use .len()
                if i < offspring.nodeSize - parent1.outputSize:
                    if i > parent1.nodeSize - parent1.outputSize:
                        node = parent2.nodes[i]
                    
                    elif i > parent2.nodeSize - parent1.outputSize:
                        node = parent1.nodes[i]

                    else:
                        choices = [parent1.nodes[i], parent2.nodes[i]]
                        node = random.choice(choices)

                else:
                    choices = [parent1.nodes[parent1.nodeSize + i - offspring.nodeSize],
                               parent2.nodes[parent2.nodeSize + i - offspring.nodeSize]]
                    node = random.choice(choices)

                offspring.nodes[i] = node

                i += 1


            i = 0
            while i < offspring.connectionSize:
                if i > parent1.connectionSize:
                    connection = parent2.connections[i]

                elif i > parent2.connectionSize:
                    connection = parent1.connections[i]

                else:
                    choices = [parent1.connections[i], parent2.connections[i]]
                    connection = random.choice(choices)

                offspring.connections[i] = connection

            
            #Sprinkle mutations
            number = random.randint(0, 100)

            if number < mutationRate:
                mutation = random.choice(listOfMutations)
                mutation(offspring)
                
            
                
            newGenomes.append(offspring)
                

        #Once everything is done, this is what the class outputs
        return newGenomes, pickledGenerationData






x = generationRunner(Genome,100,5,5,firstTime=True, genomesParameter=[])




