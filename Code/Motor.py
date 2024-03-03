from machine import Pin
import utime
 
class Stepper:
    def __init__(self, step_pin, dir_pin):
        self.step_pin = Pin(step_pin, Pin.OUT)
        self.dir_pin = Pin(dir_pin, Pin.OUT)
        
        self.step_pin.value(0)
        self.dir_pin.value(0)
        
        self.position = 0
 
    def set_speed(self, speed):
        self.delay = 1 / abs(speed)
 
    def set_direction(self, direction):
        self.dir_pin.value(direction)
 
    def move_to(self, position):
        self.set_direction(1 if position > self.position else 0)
        while self.position != position:
            self.step_pin.value(1)
            utime.sleep(self.delay)
            self.step_pin.value(0)
            self.position += 1 if position > self.position else -1
 
step_pin1 = 17
dir_pin1 = 16

step_pin2 = 19
dir_pin2 = 18

step_pin3 = 14
dir_pin3 = 15

step_pin4 = 12
dir_pin4 = 13
 
stepper1 = Stepper(step_pin1, dir_pin1)
stepper2 = Stepper(step_pin2, dir_pin2)
stepper3 = Stepper(step_pin3, dir_pin3)
stepper4 = Stepper(step_pin4, dir_pin4)
