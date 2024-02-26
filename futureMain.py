import utime
import socket
from RequestParser import RequestParser
from ResponseBuilder import ResponseBuilder
from WebConnection import WiFiConnection
from generationRunner import generationRunner
from Genome import deserializeGenomeJSON, serializeGenomes, Genome
#import multipart

# connect to WiFi
if not WiFiConnection.start_station_mode(True):
    raise RuntimeError('network connection failed')

def parse_multipart_form_data(raw_request, content_type):
    print(raw_request, content_type)
    boundary = content_type.split("boundary=")[1]
    print(boundary)
    parts = raw_request.split(boundary.encode())
    parts.pop(0)
    print(parts)
    
    

    form_data = {}
    for part in parts:
        if part.strip():  # Ignore empty parts
            header, data = part.split(b"\r\n\r\n", 1)
            header_lines = header.decode().split("\r\n")

            # Extract form field name from Content-Disposition header
            field_name = None
            for line in header_lines:
                if line.startswith("Content-Disposition:"):
                    field_name = line.split("name=")[1].strip('"')

            if field_name:
                form_data[field_name] = data[:-2]  # Remove trailing \r\n

    return form_data



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
            raw_request = cl.recv(50000)
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
                
                if request.get_header_value("Content-Type").find("multipart/form-data") != -1:
                    form_data = parse_multipart_form_data(raw_request, request.get_header_value("Content-Type"))
                    print(form_data)
                    print(1)

                    # Access form fields as dictionary
                    if form_data and "serializedGenomes" in form_data:
                        serialized_genomes = form_data["serializedGenomes"]
                        firstTime = form_data["firstTime"]
                        numberOfGenomesExpected = form_data["numberOfGenomesExpected"]
                        print(2)
                        
                        if not firstTime == "y":
                            genomes = deserializeGenomeJSON(serialized_genomes, numberOfGenomesExpected)
                            response_builder.set_body("Finished")
                            print(3)
                        else:
                            genomes = []
                            response_builder.set_body("Finished2")
                            print(4)
                    response_builder.set_body("Oopsies")
                      
                
                # if action == 'sendPickledGenomes':
                #     print(request.data())
                #     print("Hello")
                   
                #     JSONData = request.data()["serializedGenomes"]
                   
                #     firstTime = request.data()['firstTime']
                #     numberOfGenomesExpected = request.data()['numberOfGenomesExpected']
                #     print("Hello")
                  
                   
                #     if not firstTime == 'y':
                #         print("Not firsttime")
                #         print(f"Json Data: {JSONData}")
                        
                        
                #         genomes = deserializeGenomeJSON(JSONData, numberOfGenomesExpected)
                #         response_builder.set_body("Finished1")
                #     else:
                #         print(f"JOSN Data: {JSONData}")
                #         print("First Time")
                #         genomes = []
                #         response_builder.set_body("Finished2")
                    
                  

                    

    
                elif action == 'sendHyperParameters':
                    mutationRate = int(request.data()["mutationRate"])
                    numberOfGenomes = int(request.data()["numberOfGenomes"])
                    percentageToDrop = int(request.data()["percentageToDrop"])
                    iterationsAllowed = int(request.data()["iterationsAllowed"])

                    if firstTime == "y":
                        generation = generationRunner(Genome, numberOfGenomes, percentageToDrop, mutationRate, genomes, True)
                    else:
                        generation = generationRunner(Genome, numberOfGenomesExpected, percentageToDrop, mutationRate, genomes, False)
                    

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
                        
                        newGenomes, pickledGenerationData = generation.afterGenomesRan()
                        print("HI")

                        postData = {
                            "moreGenomes": "no",
                            "newGenomes": newGenomes,
                            "pickledGenerationData": pickledGenerationData
                        }
                        
                        print("HELLO")

                        response_builder.set_body_from_dict(postData)
                        
                        print("BYE")

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

                    response_builder.set_body("Finished")

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
