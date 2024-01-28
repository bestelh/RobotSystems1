import atexit
import time
from picarx_improved import Picarx

try:
    from robot_hat import ADC   
except ImportError:
    from sim_robot_hat import ADC

class Sensing():

    def __init__(self):
        self.pin1, self.pin2, self.pin3 = ADC('A0'), ADC('A1'), ADC('A2')

    def read_pins(self):
        return self.pin1, self.pin2, self.pin3

if __name__ == "__main__":
    sensor = Sensing()
    while True:
        print(sensor.read_pins())
        time.sleep(0.1)  # Wait for 0.1 seconds
        command = input("Enter command: ")
        if command.upper() == 'EXIT':
            break