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



## January 10, 2024 *Note: Files for this date were regrettingly forgotton to upload*
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
> 

## January 13, 2024
### 8:45 pm

I got a lot of code done today. Most notably would be the new mutations file. This morning, I filled the mutations file with 9 mutations. They include the mutations to add nodes, connections, and gaters; the mutations to modify weights, biases, and activation functions (In the cited source on the project proposal, the activation functions are commonly referred to as squashes. I refer to them in my code as activation functions.); and the mutations to remove nodes, connections, and gaters.

I also finished the cross-breeding:

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
                # Make output nodeSize  and connectionSize variable in genome class WRONG WRONG WRONG use .len() in the future
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

>This code is in a loop that creates more offspring until the required amount is met. First, it randomly assigns two parents. Then, it initiates the offspring genome. Then it determines the size of the offspring: the parent with the highest fitness passes on the size. After, it assigns the nodes and connections. Finally, it adds mutations and adds the new genome to the new genomes list.
>
I tweaked some things in the genome class. The most notable are the new methods: findOutgoingConnections, findIncomingConnections, and areNodesConnected. The names are pretty self-expanatory. They all take nodes as parameters.
I am nearing the final stretch of the coding process.



## January 14, 2024
### 8:30 pm

The most notable thing I worked on today was the client-side of the project. I improved on the HTML file, as well as added a javascript file and a css file. It is not completely done, but progress is being made. I also made some tweaks. I am trying to figure out how to make the generationRunner work better. My vision is that there is an instance for each generation. Tomorrow, I am going to test if the http request handler works.

## January 15-17, 2024
### 3:30 pm

Over the past few days, I am altered the code and tested it with the raspberry pi pico. A big change would be to the main.py file. Previously, it was using asyncronous programming and used both cores. Now I realise that those are not nessacery and simplified it. There is a line of blocking code, but it shouldn't matter. The motor class still exists, though I am getting the feeling that the IoHandler file will take over in somepoint in the future. Don't really know why I uploaded the dummyCode file. The generationRunner file added a new method. It determines which gemone should be ran. Also, the runOneGenome method got upgraded.
Also, I had to reset my pico because I put a while loop inside a file named main. It is annoying, because I lost some files. I uploaded the files again, but some changes were lost.

## January 20-ish, 2024

Technically I am writing this on 2/2/2024, but I forgot to add that I finished the javascript file. It handled requests on the client side and interacted with the webpage accordingly.

## Febrary 2, 2024
### 5:00 pm

Over the past few days, I have been gathering parts to begin the constuction of the physical model. I have been having some trouble moving the motor until today. I mixed up the wires! Today I should also upload more files.

## Febrary 4, 2024
### 10:30 am

I spent yesterday perfecting the 3d model for the bot. The annoying part was making sure it fit inside the printer. I found [this](https://www.formware.co/OnlineStlRepair) website incredibly helpful for repairing the stl file (making sure that the file can be printed accurately). I left the printer on overnight and it finished printing at around 9:15 am. 

>![F2D33B98-DA3E-44E5-A37D-0B0055AA6B29](https://github.com/Georgie-design/Science-Fair-Neuroevolution/assets/125774486/94ac5616-c7ad-488d-96ec-f84be88a0549)
> Currently it has supports, and weighs 151 grams.

>![image](https://github.com/Georgie-design/Science-Fair-Neuroevolution/blob/main/BotPhotos/90B13EFA-0A0D-4F09-93C0-790147C1D13B.jpeg)
> With supports removed, it only weighs 85 grams

>![image](https://github.com/Georgie-design/Science-Fair-Neuroevolution/blob/main/BotPhotos/03C864BF-7783-4051-9585-EC5CA1FD7C0B.jpeg)
> With some circuitry added, problems began to emerge. The battery case holders were not wide enough and the towers that were supposed to be holding them in were to fragile (in the photo, most have broken off). The breadboard space was a tight squeeze, so that will need to be widened. The motors fit perfectly. I might also consider thickening the walls to ensure that it will not break. And finally, I will probably make the corrdinate holes on the side smaller for more percision when measuring the distance it has traveled.
>


## February 10, 2024
### 10:00 pm

I just finished the revised design. It will take 17 hours to print, so I am getting it ready over night. Best of luck.

## February 19, 2024
### 8:30 pm

It has been a while since the last check-in. I only worked on hardware during this time. The new design has worked perfectly (however, I noted that the space for the breadboard was hard to get to. If I am ever going to make something like this again, I should remember to put the breadboard/circuitry on the top for better access). I have found [this](https://how2electronics.com/control-stepper-motor-with-a4988-raspberry-pi-pico/) circuit diagram immensely helpful. It only connects to 1 motor, so I quadrupled the design on my breadboard. At some point, I will add my own diagram.
The struggle has been checking for loose wires and making sure everything is in the right spot, and as of right now everything appears in order. I will be ramping up my project time in order to meet the upcoming deadline.

