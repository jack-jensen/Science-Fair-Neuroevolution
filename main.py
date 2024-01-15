# POSTER BOARD IDEA: ONE SIDE IS HARDWARE AND THE OTHER IS SOFTWARE. CENTER IS ABSTRAcT

#ADD GATERS TO THE CONNECTIONS


#USE PICKLE TO SAVE OBJECTS TO FILE FOR LATER RETRIEVAL

import uasyncio
import _thread
from Genome import Genome
from WebConnection import WiFiConnection
from generationRunner import generationRunner
from RequestParser import RequestParser
from ResponseBuilder import ResponseBuilder
from IoHandler import IoHandler

if not WiFiConnection.start_station_mode(True):
    raise RuntimeError('network connection failed')

async def handle_request(reader, writer):
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


                response_builder.set_body_from_dict(generationData)

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
            response_builder.serve_static_file(request.url)

        response_builder.build_response()
        writer.write(response_builder.response)
        await writer.drain()
        await writer.wait_closed()

            
    except OSError as e:
        print('connection error ' + str(e.errno) + " " + str(e))



async def main():
    print('Setting up webserver...')
    server = uasyncio.start_server(handle_request, "0.0.0.0", 80)
    uasyncio.create_task(server)

    # main async loop on first core
    # just pulse the red led
    counter = 0
    while True:
        if counter % 500 == 0:
            IoHandler.toggle_pico_led()
        counter += 1
        await uasyncio.sleep(0)
 


def secondThreadMethod():
    pass


# start neopixel scrolling loop on second processor
second_thread = _thread.start_new_thread(secondThreadMethod, ())

try:
    # start asyncio tasks on first core
    uasyncio.run(main())
finally:
    print("running finally block")
    uasyncio.new_event_loop()



