from machine import Pin

class IoHandler:
    def __init__():
        pass
    
    
    @staticmethod
    def toggleLED():
        led = Pin("LED", Pin.OUT)
        timer = Timer()
        led.toggle()


