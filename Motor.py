from dummyCode import Pin

class Motor:
    def __init__(self, firstCoil_1_p, firstCoil_2_p, secondCoil_1_p, secondCoil_2_p):
        self.firstCoil_1 = Pin(firstCoil_1_p, Pin.OUT)
        self.firstCoil_2 = Pin(firstCoil_2_p, Pin.OUT)
        self.secondCoil_1 = Pin(secondCoil_1_p, Pin.OUT)
        self.secondCoil_2 = Pin(secondCoil_2_p, Pin.OUT)

    def runClockwiseOnePhase(self):
        # blah
        # blah
        # blah
        pass
    
    def runCounterclockwiseOnePhase(self):
        # blah
        # blah
        # blah
        pass

    def stop(self):
        self.firstCoil_1.value(0)
        self.firstCoil_2.value(0)
        self.secondCoil_1.value(0)
        self.secondCoil_2.value(0)

    def runClockwiseTEST(self):
        pass

    def runCounterclockwiseTest(self):
        pass