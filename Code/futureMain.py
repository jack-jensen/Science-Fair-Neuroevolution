import socket
from RequestParser import RequestParser
from ResponseBuilder import ResponseBuilder
from WebConnection import WiFiConnection
from generationRunner import generationRunner

if not WiFiConnection.start_station_mode(True):
    raise RuntimeError('network connection failed')

def beginProgram():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('listening on', addr)

    newGenomes = []
    while True:
        cl = False
        try:
            cl, addr = s.accept()
            raw_request = cl.recv(1024)
            print(raw_request)

            request = RequestParser(raw_request)
            response_builder = ResponseBuilder()
            
            if request.url_match("/api"):
                action = request.get_action()
                print(action)
                print(request.data())
                
                if action == 'sendHyperParameters':
                    mutationRate = int(request.data()["mutationRate"])
                    numberOfGenomes = int(request.data()["numberOfGenomes"])
                    percentageToDrop = int(request.data()["percentageToDrop"])
                    iterationsAllowed = int(request.data()["iterationsAllowed"])

                    generation = generationRunner(numberOfGenomes, percentageToDrop, mutationRate, newGenomes)
            
                elif action == 'runOneGenome':
                    nextGenome = generation.findNextGenome()
                    if nextGenome != None:
                        outputData = generation.runOneGenome(nextGenome, iterationsAllowed)
                        postData = {
                            "moreGenomes": "yes",
                            "data": outputData,
                            "identificationNumber": nextGenome.identificationNumber
                        }

                        response_builder.set_body_from_dict(postData)
                    else:
                        newGenomes, serializednewGenomes, pickledGenerationData = generation.afterGenomesRan()
                        
                        del generation
                        generation = generationRunner(numberOfGenomes, percentageToDrop, mutationRate, newGenomes)
                        
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
                    print("Unknown Action")
                    response_builder.set_status(404)

            else:
                response_builder.serve_static_file(request.url, "/index.html")

            response_builder.build_response()
            sent = cl.write(response_builder.response)
            cl.close()

        except OSError as e:
            cl.close()
            print(e)
            print('connection closed')

beginProgram()
