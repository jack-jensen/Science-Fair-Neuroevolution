#ADD GATERS TO THE CONNECTIONS


#USE PICKLE TO SAVE OBJECTS TO FILE FOR LATER RETRIEVAL

import uasyncio
import _thread
from Genome import Genome
from WebConnection import WiFiConnection
from generationRunner import generationRunner

if not WiFiConnection.start_station_mode(True):
    raise RuntimeError('network connection failed')

def handleRequests(reader, writer):
    try:
        raw_request = await reader.read(2048)

        request = RequestParser(raw_request)

        response_builder = ResponseBuilder()

        if request.url_match("/api"):
            action = request.get_action()
            if action == "initiateProcess":
                message = "You have initiated the start-up sequence. Place automation in the center of the degree map"
                response_builder.set_body(message)

            elif action == "greenLight":
                #Figure out how to use async with this, as the process will most likely take a while

                newGenomes, generationData = generationRunner()
                response.set_body_from_dict(generationData)

            elif action == "abandonShip":
                #halt robot
                pass
            elif action == "pause":
                #Figure out how to pause the automation
                pass
            else:
                #Unknown action
                actions = ["initiateProcess", "greenLight", "abandonShip", "pause"]
                raise RuntimeError(f"ERROR!!! Called for unknown action. The avaliable actions are {actions}")
        else:
            #This probably means that they just visted the webserver from the browser
            response_builder.serve_static_file(request.url, "/index.html")

            
    except:
        

        pass








genome = Genome()
