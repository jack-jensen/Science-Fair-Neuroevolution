# LOG

## December 31, 2023
### 12:30 pm

I have just created the activations folder and painstakenly filled it with the functions suggested by the cited sources. I created in another file to clean out the main file, which is growing rapidly. In the past week, I have began 
 to constructed the motor and genome classes. I also added some dummy code for the pin class. This will not actually be used in practice, as micropython supplies a module to controll the pins on the microcontroller. 
So far, the motor class initiates the pins for the motor and has some function skeletons for me to code later. I will initiate this class for all four motors when the time comes. On the other hand, for the genome class, 
it contains two arrays for the nodes and connections. The array contains the node and connection child class objects. I have added the code to initiate the first input and output nodes, as well as the connections. The connections are
assigned to nodes randomly. If a node is connected to itself, then a boolean in the connection object is switched to true. I am not sure if this will be needed, but the cited sources did mention that self-connections are handled 
differently. In order to control the order that the nodes get activated, I have added an index calculator function that assigns a unique number to each node. I will also have to find out which of the connections gets activated first,
however!


## January 2, 2024
### 10:45 am

Yesterday, I began construction on the evaluationGenome function (in doing this, I also added some more variables to the node and connection classes), which looks like this right now:


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


> First, it sorts the nodes by index. Then, it runs a while loop for the maximum amount of iterations the genome can run. Then it iterates through each node. If the node is an input, then the activation of that node is simply the input.
Otherwise, it then iterates through each of the connections. If it is a self-connection, then it is handled differently. If the node is an output, then if will probably be added to the motors, but that haesn't been coded yet. I also added
> some notes for me later.

Then, I created some files to store the html for the dashboard and a file that contains the code to interact with it. There is nothing in there yet.



## January 10, 2024
### 5:30 pm

In the past few days, I have been researching how to make a dashboard for my project. I found an extremely helpful [video](https://www.youtube.com/watch?v=h18LMskRNMA&list=PLvOT6zBnJyYFqKp4dBCS1aZ8Nzbll7qre&index=6), and ended up using code from the video in my project. The files ResponseBuilder.py, ResponseParser.py, and WebConnection.py are all completely not my code. I also used their code as a framwork for main.py. This code is only used for communicating with the webserver. All project-specific code is my own.

I moved the motor and genome classes to their own files, and I added some files to hold network credientials and dummy code. Big changes I've added include that in the main file I added the handleRequests method, which is based on the code from the tutorial mentioned above. I tweaked the code and the actions to match my own project. Right now, it is a mess. Also, I created the generationRunner class, which will run a generation. Here is that code so far:

    from Genome import Genome
    import random
    #After each indivitaul run is complete, ask if they need to pause
    
    class generationRunner:
        def __init__(self, numberOfGenomes, percentageToDrop):
            genomes = [Genome(i) for i in numberOfGenomes]
        
            rankedGenomes = genomes.sort(genomes, key=lambda item:item.fitness)
    
            #Save rankedGenomes list - with all the class genome objects
    
    
            #You may not have to eliminate the genomes. Reproduce all the genomes randomly, then the last
            # generation 'dies'.
            numberToEliminate = round(numberOfGenomes / percentageToDrop)
    
            for i in range(numberToEliminate):
                rankedGenomes.pop()
    
    
            while numberOfGenomes < len(rankedGenomes):
    
                offspring = Genome()
                while parent1 != parent2:
                    parent1 = random.choice(rankedGenomes)
                    parent2 = random.choice(rankedGenomes)
                
                if parent1.size > parent2.size:
                    offspring.size
    
    
                
                pass
    
            #Sprinkle mutations
    
            #Once everything is done, this is what the class outputs
            return newGenomes, generationData

> This code is based on the cited source in the project proposal
> It initiates all the genomes state. Later, I will add the code that runs the genome objects. After, the genomes are ranked based on how well their fitness score is. I have added some notes, but currently the plan is to eliminate a certain number of genomes. Then I am currently working on add the crossbreeding. Right now all it does is randomly select two 'parent' genomes.
