# This is the file that is actually run on the computer.
import socket
from RequestParser import RequestParser
from ResponseBuilder import ResponseBuilder
from WebConnection import WiFiConnection
from generationRunner import generationRunner

# This connects to the wifi.
if not WiFiConnection.start_station_mode(True):
    raise RuntimeError('network connection failed')

def beginProgram():
    # This creates a socket, which means that
    # it is connecting to the ip.
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('listening on', addr)

    newGenomes = []
    while True:
        cl = False
        try:
            # This creates the client/server relationship, which means
            # that I can now communitcate with the server with http requests on a browser.
            # This line of code waits until a request comes in.
            cl, addr = s.accept()
            raw_request = cl.recv(1024) # Number of bytes the request can be
            print(raw_request)

            # These classes are not my code. They help for reading and writing http requests.
            request = RequestParser(raw_request)
            response_builder = ResponseBuilder()
            
            # This runs if the http request is trying to run something on the server.
            if request.url_match("/api"):
                action = request.get_action()
                print(action)
                print(request.data())
                
                # The action stated in the http request is detected here.
                if action == 'sendHyperParameters':
                    # This is run when the hyperparameters form is submited on the browser.
                    # First, it gets all the data from the request.
                    mutationRate = int(request.data()["mutationRate"])
                    numberOfGenomes = int(request.data()["numberOfGenomes"])
                    percentageToDrop = int(request.data()["percentageToDrop"])
                    iterationsAllowed = int(request.data()["iterationsAllowed"])

                    # Then, it initializes the first generation with the hyperparameters.
                    generation = generationRunner(numberOfGenomes, percentageToDrop, mutationRate, newGenomes)
            
                elif action == 'runOneGenome':
                    # This is run when the client (browser) has given the green light for the
                    # automation to run. First, it determines which genome is next.
                    nextGenome = generation.findNextGenome()
                    
                    if nextGenome != None:
                        # This function runs the genome and returns the output data.
                        outputData = generation.runOneGenome(nextGenome, iterationsAllowed)
                        
                        # This dictionary gets the data to send back to the browser to be downloaded.
                        postData = {
                            "moreGenomes": "yes",
                            "data": outputData,
                            "identificationNumber": nextGenome.identificationNumber
                        }

                        response_builder.set_body_from_dict(postData)
                    else:
                        # If all the genomes in a generation has been run, then it runs a function which returns
                        # the newGenomes and the data. The serializednewGenomes has the new genomes in json
                        # format for easy recovery later. The pickledGenerationData is the same except
                        # that it contains the old genomes with all their data.
                        newGenomes, serializednewGenomes, pickledGenerationData = generation.afterGenomesRan()
                        
                        # It deletes the previous generation for memory purposes, then makes the new generation
                        # with the new genomes.
                        del generation
                        generation = generationRunner(numberOfGenomes, percentageToDrop, mutationRate, newGenomes)
                        
                        # Then it sends the data back to the browser.
                        postData = {
                            "moreGenomes": "no",
                            "newGenomes": serializednewGenomes,
                            "pickledGenerationData": pickledGenerationData
                        }
                    
                        response_builder.set_body_from_dict(postData)
                    
                elif action == "sendFitnessData":
                    # This is run when the browser submits the fitness form data. 
                    # First, it recovers the coordinate data.
                    x1 = float(request.data()["x1"])
                    y1 = float(request.data()["y1"])
                    x2 = float(request.data()["x2"])
                    y2 = float(request.data()["y2"])
                    identificationNumber = int(request.data()["identificationNumber"])

                    # Then it figures out which genome the coordinate data belongs to with the
                    # identification number.
                    for genome in generation.genomes:
                        if genome.identificationNumber == identificationNumber:
                            fitness = genome.calculateFitness(x1, y1, x2, y2)
                            genome.fitness = fitness
                            break

                else:
                    # If the action isn't listed above, then the program returns an error.
                    print("Unknown Action")
                    response_builder.set_status(404)

            else:
                # If it isn't trying to run something specific, then that probably
                # means that the client just went on the site and is asking for the webpage.
                response_builder.serve_static_file(request.url, "/index.html")

            # It builds the response
            response_builder.build_response()
            sent = cl.write(response_builder.response)
            cl.close()

        except OSError as e:
            cl.close()
            print(e)
            print('connection closed')

beginProgram()
