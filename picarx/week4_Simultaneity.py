import time
from picarx_improved import Picarx
import atexit
import concurrent.futures
from readerwriterlock import rwlock

try:
    from robot_hat import ADC   
except ImportError:
    from sim_robot_hat import ADC

px = Picarx()

class Bus:
    def __init__(self):
        self.message = None
        self.lock = rwlock.RWLockWriteD()

    def write(self, message):
        with self.lock.gen_wlock():
            self.message = message

    def read(self, message):
        with self.lock.gen_rlock():
            message = self.message
        return self.message

class Sensing():
    def __init__(self):
        self.chn_0 = ADC('A0')
        self.chn_1 = ADC('A1')
        self.chn_2 = ADC('A2')

    def get_grayscale_data(self):
        adc_value_list = []
        adc_value_list.append(self.chn_0.read())
        adc_value_list.append(self.chn_1.read())
        adc_value_list.append(self.chn_2.read())
        return adc_value_list

    def sensor(self, bus, delay):
        while True:
            bus.write(self.get_grayscale_data())
            time.sleep(delay)

class Interpreter():
    def __init__(self,sensitivity=0.7, polarity=-1):
        self.sensitivity = sensitivity
        self.polarity = polarity

    def interpret(self, readings):
        avg = sum(readings) / len(readings)
        if self.polarity == 1:
            return [1 if (reading - avg) > self.sensitivity else 0 for reading in readings]
        else:
            return [0 if (reading - avg) > self.sensitivity else 1 for reading in readings]

    def map_readings_to_value(self,readings):
        if readings == [0, 1, 0]:
            return 0
        elif readings == [0, 1, 1]:
            return 0.5
        elif readings == [0, 0, 1]:
            return 1
        elif readings == [1, 1, 0]:
            return -0.5
        elif readings == [1, 0, 0]:
            return -1

    def interpreter(self, bus_sensor, bus_control, delay):
        while True:
            readings = bus_sensor.read()
            interpreted = self.map_readings_to_value(self.interpret(readings))
            bus_control.write(interpreted)
            time.sleep(delay)

class Controller():
    def __init__(self,scaling=1.0):
        self.scaling = scaling

    def control(self, value):
        if value == 0:
            px.set_dir_servo_angle(0)
        elif value == 1:
            px.set_dir_servo_angle(30*self.scaling)
        elif value == -1:
            px.set_dir_servo_angle(-30*self.scaling)

    def controller(self, bus, delay):
        while True:
            self.control(bus.read())
            time.sleep(delay)

if __name__ == "__main__":
    bus_sensor = Bus()
    bus_control = Bus()
    sensing = Sensing()
    interpreter = Interpreter(sensitivity=0.95, polarity=1)
    controller = Controller(scaling=1)
    delay=0.01
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        eSensor = executor.submit(sensing.sensor, bus_sensor, delay)
        eInterpreter = executor.submit(interpreter.interpreter, bus_sensor, bus_control, delay)
        eController = executor.submit(controller.controller, bus_control, delay)
eSensor.result()
