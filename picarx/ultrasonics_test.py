import time
from picarx_improved import Picarx
import atexit

try:
    from robot_hat import ADC   
except ImportError:
    from sim_robot_hat import ADC

px = Picarx()

class Ultrasonic_Sensing():
    def __init__(self, timeout=0.02):
        self.trig = 'D2'
        self.echo = 'D3'
        self.timeout = timeout

    def _read(self):
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
        cm = round(during * 340 / 2 * 100, 2)
        return cm

    def read(self, times=10):
        for i in range(times):
            a = self._read()
            if a != -1:
                return a
        return -1
    
if __name__ == "__main__":
    ult_sense = Ultrasonic_Sensing()
    while True:
        
        print(ult_sense.read())
        time.sleep(0.5) 
