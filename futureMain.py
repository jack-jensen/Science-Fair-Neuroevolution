
import utime
import socket
from RequestParser import RequestParser
import _thread
from ResponseBuilder import ResponseBuilder
from WebConnection import WiFiConnection
import random
import mip
from generationRunner import generationRunner
from Genome import unPickleGenomeFile, Genome
import pickle

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
                # read api action requested
                action = request.get_action()
                if action == 'sendPickledGenomes':
                    print(request.data())
                   
                    rawFile = request.data()["file"]
                   
                    firstTime = request.data()['firstTime']
                    numberOfGenomesExpected = request.data()['numberOfGenomesExpected']
                  
                   
                    if not firstTime == 'y':
                        
                        
                        genomes = unPickleGenomeFile(rawFile, numberOfGenomesExpected)
                        if genomes == "Error":
                            response_builder.set_body("Error")
                        else:

                            response_builder.set_body("Finished1")
                    else:
                        genomes = []
                        response_builder.set_body("Finished2")
                    
                  

                    

    
                elif action == 'sendHyperParameters':
                    mutationRate = int(request.data()["mutationRate"])
                    numberOfGenomes = int(request.data()["numberOfGenomes"])
                    percentageToDrop = int(request.data()["percentageToDrop"])

                    if firstTime == "y":
                        generation = generationRunner(Genome, numberOfGenomes, percentageToDrop, mutationRate, genomes, True)
                    else:
                        generation = generationRunner(Genome, numberOfGenomesExpected, percentageToDrop, mutationRate, genomes, False)
                    

                elif action == 'runOneGenome':
                    nextGenome = generation.findNextGenome()
                    if nextGenome != None:
                        outputData = generation.runOneGenome(nextGenome)
                        postData = {
                            "moreGenomes": "yes",
                            "data": outputData,
                            "identificationNumber": nextGenome.identificationNumber
                        }

                        response_builder.set_body_from_dict(postData)
                    else:
                        
                        newGenomes, pickledGenerationData = generation.afterGenomesRan()

                        postData = {
                            "moreGenomes": "no",
                            "newGenomes": newGenomes,
                            "pickledGenerationData": pickledGenerationData
                        }

                        response_builder.set_body("No more Genomes")

                elif action == "sendFitnessData":
                    distance = request.data()["distance"]
                    identificationNumber = int(request.data()["identificationNumber"])

                    for genome in generation.genomes:
                        if genome.identificationNumber == identificationNumber:
                            fitness = genome.calculateFitness(distance)
                            genome.fitness = fitness
                            break

                    response_builder.set_body("Finished")

                else:
                    # unknown action - send back not found error status
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





