import socket
from RequestParser import RequestParser
from ResponseBuilder import ResponseBuilder
from WebConnection import WiFiConnection
from generationRunner import generationRunner
from Genome import Genome
#import multipart

# connect to WiFi
if not WiFiConnection.start_station_mode(True):
    raise RuntimeError('network connection failed')



def beginProgram():

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)

    # main web server loop
    newGenomes = []
    while True:
        cl = False
        try:
            # wait for HTTP request
            cl, addr = s.accept()
            # print('client connected from', addr)
            raw_request = cl.recv(1024)
            print(raw_request)

            # parse HTTP request
            request = RequestParser(raw_request)
            #print(request.method, request.url, request.get_action())

            # Prepare to build HTTP response
            response_builder = ResponseBuilder()

            # filter out api request
            if request.url_match("/api"):
                print("Happy Birthday")
                # read api action requested
                action = request.get_action()
                print(action)
                print(request.data())
                
            
                    

    
                if action == 'sendHyperParameters':
                    mutationRate = int(request.data()["mutationRate"])
                    numberOfGenomes = int(request.data()["numberOfGenomes"])
                    percentageToDrop = int(request.data()["percentageToDrop"])
                    iterationsAllowed = int(request.data()["iterationsAllowed"])


                    generation = generationRunner(Genome, numberOfGenomes, percentageToDrop, mutationRate, newGenomes)
                    

                elif action == 'runOneGenome':
                    nextGenome = generation.findNextGenome()
                    if nextGenome != None:
                        print(nextGenome)
                        outputData = generation.runOneGenome(nextGenome, iterationsAllowed)
                        postData = {
                            "moreGenomes": "yes",
                            "data": outputData,
                            "identificationNumber": nextGenome.identificationNumber
                        }

                        response_builder.set_body_from_dict(postData)
                    else:
                        print(nextGenome)
                        
                        newGenomes, serializednewGenomes, pickledGenerationData = generation.afterGenomesRan()
                        
                        del generation
                        generation = generationRunner(Genome, numberOfGenomes, percentageToDrop, mutationRate, newGenomes)
                        

                        postData = {
                            "moreGenomes": "no",
                            "newGenomes": serializednewGenomes,
                            "pickledGenerationData": pickledGenerationData
                        }
                    

                        response_builder.set_body_from_dict(postData)
                    

                elif action == "sendFitnessData":
                    x1 = float(request.data()["x1"])
                    y1 = float(request.data()["y1"])
                    x2 = float(request.data()["x2"])
                    y2 = float(request.data()["y2"])
                    identificationNumber = int(request.data()["identificationNumber"])

                    for genome in generation.genomes:
                        if genome.identificationNumber == identificationNumber:
                            fitness = genome.calculateFitness(x1, y1, x2, y2)
                            genome.fitness = fitness
                            break

                else:
                    # unknown action - send back not found error status
                    print("unkown Action")
                    response_builder.set_status(404)

            # try to serve static file
            else:
                # return file if valid
                response_builder.serve_static_file(request.url, "/index.html")

            # build the HTTP response
            response_builder.build_response()
            # return response to client
            sent = cl.write(response_builder.response)
            cl.close()

        except OSError as e:
            cl.close()
            print(e)
            print('connection closed')

# main control loop

beginProgram()
