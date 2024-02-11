import time
from picarx_improved import Picarx
import atexit

try:
    from robot_hat import Pin, ADC
except ImportError:
    from sim_robot_hat import ADC

px = Picarx()

class Ult_Sensing():
    def __init__(self, timeout=0.02):
        self.trig = Pin('D2')
        self.echo = Pin('D3')
        self.timeout = timeout

    def get_ultrasonic_data(self):
        self.trig.low()
        time.sleep(0.01)
        self.trig.high()
        time.sleep(0.00001)
        self.trig.low()
        pulse_end = 0
        pulse_start = 0
        timeout_start = time.time()
        while self.echo.value()==0:
            pulse_start = time.time()
            if pulse_start - timeout_start > self.timeout:
                return -1
        while self.echo.value()==1:
            pulse_end = time.time()
            if pulse_end - timeout_start > self.timeout:
                return -1
        during = pulse_end - pulse_start
        return during
    
    def read(self):
        return self.get_ultrasonic_data()

class Ult_Interpreting():
    def __init__(self):
        pass

    def interpret(self, data):
        if data == -1:
            return -1000
        cm = round(data * 340 / 2 * 100, 2)
        return cm
    
class Ult_Control():
    def _init_(self):
        pass

    def controller(self, threshold,speed):
        if threshold < 10:
            px.forward(0)
            px.stop
        else:
            px.forward(speed)
            

    
if __name__ == "__main__":
    ult_sensing=Ult_Sensing()
    ult_interp = Ult_Interpreting()
    ult_control= Ult_Control()
    try:
        while True:
            speed=35
            ult_control.controller(ult_interp.interpret(ult_sensing.read()),speed)
            print(ult_interp.interpret(ult_sensing.read()))
            time.sleep(0.5) 
    except KeyboardInterrupt:
            px.stop()