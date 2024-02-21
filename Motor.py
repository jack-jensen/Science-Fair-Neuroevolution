from machine import Pin
import utime
 
class Stepper:
    def __init__(self, step_pin, dir_pin):
        self.step_pin = Pin(step_pin, Pin.OUT)
        self.dir_pin = Pin(dir_pin, Pin.OUT)
        self.position = 0
 
    def set_speed(self, speed):
        self.delay = 1 / abs(speed)  # delay in seconds
 
    def set_direction(self, direction):
        self.dir_pin.value(direction)
 
    def move_to(self, position):
        self.set_direction(1 if position > self.position else 0)
        while self.position != position:
            self.step_pin.value(1)
            utime.sleep(self.delay)
            self.step_pin.value(0)
            self.position += 1 if position > self.position else -1
 
# Define the pins
step_pin1 = 17  # GPIO number where step pin is connected
dir_pin1 = 16   # GPIO number where dir pin is connected

step_pin2 = 19
dir_pin2 = 18

step_pin3 = 14
dir_pin3 = 15

step_pin4 = 12
dir_pin4 = 13
 
# Initialize stepper
stepper1 = Stepper(step_pin1, dir_pin1)
stepper2 = Stepper(step_pin2, dir_pin2)
stepper3 = Stepper(step_pin3, dir_pin3)
stepper4 = Stepper(step_pin4, dir_pin4)
 
def loop():
    while True:
        # Move forward 2 revolutions (400 steps) at 200 steps/sec
        stepper1.set_speed(100)
        stepper1.move_to(400)
        print(1)
        utime.sleep(1)
        
        
        stepper2.set_speed(100)
        stepper2.move_to(400)
        print(2)
        utime.sleep(1)
 
        # Move backward 1 revolution (200 steps) at 600 steps/sec
        stepper1.set_speed(100)
        stepper1.move_to(200)
        print(3)
        utime.sleep(1)
        
        stepper2.set_speed(100)
        stepper2.move_to(200)
        print(4)
        utime.sleep(1)
 
        # Move forward 3 revolutions (600 steps) at 400 steps/sec
        stepper1.set_speed(100)
        stepper1.move_to(600)
        print(5)
        utime.sleep(1)
        
        stepper2.set_speed(100)
        stepper2.move_to(600)
        print(6)
        utime.sleep(3)
 
# if __name__ == '__main__':
#     loop()