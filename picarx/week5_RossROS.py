import rossros as rr
import logging
import time
import math
import time
from picarx_improved import Picarx
from readerwriterlock import rwlock

try:
    from robot_hat import ADC
    from robot_hat.utils import reset_mcu, run_command
except ImportError:
    from sim_robot_hat import ADC
    from sim_robot_hat import reset_mcu, run_command

# logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.INFO)

px = Picarx()

""" First Part: Signal reading and processing functions """

class Sensing():

    def __init__(self):
            self.chn_0 = ADC('A0')
            self.chn_1 = ADC('A1')
            self.chn_2 = ADC('A2')

    def get_grayscale_data(self):
        adc_value_list = []
        adc_value_0 = self.chn_0.read()
        adc_value_1 = self.chn_1.read()
        adc_value_2 = self.chn_2.read()
        print(f"ADC values: {adc_value_0}, {adc_value_1}, {adc_value_2}")
        adc_value_list.append(adc_value_0)
        adc_value_list.append(adc_value_1)
        adc_value_list.append(adc_value_2)
        return adc_value_list

      
    def read(self):
        return self.get_grayscale_data()

class Interpreter():
     
    def __init__(self,sensitivity=0.7, polarity=-1):
        self.sensitivity = sensitivity
        self.polarity = polarity
    
    def process_sensor_data(self, readings):
        # Interpret the readings
        avg = sum(readings) / len(readings)
        if self.polarity == 1:
            interpreted_readings = [1 if (reading - avg) > self.sensitivity else 0 for reading in readings]
        else:
            interpreted_readings = [0 if (reading - avg) > self.sensitivity else 1 for reading in readings]

        # Map the interpreted readings to a value
        if interpreted_readings == [0, 1, 0]:
            return 0
        elif interpreted_readings == [0, 1, 1]:
            return 0.5
        elif interpreted_readings == [0, 0, 1]:
            return 1
        elif interpreted_readings == [1, 1, 0]:
            return -0.5
        elif interpreted_readings == [1, 0, 0]:
            return -1
        elif interpreted_readings == [1, 1, 1]:
            return 0
        elif interpreted_readings == [0, 0, 0]:
            return 0
        else:
            return None  # Return None if the interpreted readings do not match any known pattern

class Controller():
    def __init__(self,scaling=1.0):
        self.scaling = scaling

    def control(self, value):
        #print(f"Controller is processing value: {value}")
        if value == 0:
            px.set_dir_servo_angle(0)
        elif value == 1:
            px.set_dir_servo_angle(30*self.scaling)
        elif value == -1:
            px.set_dir_servo_angle(-30*self.scaling)
        elif value == -0.5:
            px.set_dir_servo_angle(-30*self.scaling)
        elif value == 0.5:
            px.set_dir_servo_angle(30*self.scaling)

""" Second Part: Create buses for passing data """
sensor = Sensing()
interpreter = Interpreter(sensitivity=0.95, polarity=-1) #light line (-1) , dark line (1)
controller=Controller(scaling=1)

# Initiate data and termination busses
bSensing = rr.Bus(sensor.read(), "Sensing bus")
bInterpreter = rr.Bus(interpreter.process_sensor_data(sensor.read()), "Interpreter Bus")
bController = rr.Bus(controller.control(interpreter.process_sensor_data(sensor.read())), "Controller bus")
bTerminate = rr.Bus(0, "Termination Bus")

""" Third Part: Wrap functions into RossROS objects """

# Wrap the sensing greyscale data into a producer
readPins = rr.Producer(
    sensor.get_grayscale_data,  # function that will generate data
    bSensing,  # output data bus
    0.01,  # delay between data generation cycles
    bTerminate,  # bus to watch for termination signal
    "Read pin data from greyscale module")

# Wrap the multiplier function into a consumer-producer
interpretData = rr.ConsumerProducer(
    interpreter.process_sensor_data,  # function that will process data
    bSensing,  # input data buses
    bInterpreter,  # output data bus
    0.05,  # delay between data control cycles
    bTerminate,  # bus to watch for termination signal
    "Multiply Waves")

# Wrap the multiplier function into a consumer-producer
controlServo = rr.Consumer(
    controller.control,  # function that will process data
    bInterpreter,  # input data buses
    0.5,  # delay between data control cycles
    bTerminate,  # bus to watch for termination signal
    "Multiply Waves")

""" Fourth Part: Create RossROS Printer and Timer objects """

# Make a printer that returns the most recent wave and product values
printBuses = rr.Printer(
    (bSensing, bInterpreter, bTerminate),  # input data buses
    # bMultiplied,      # input data buses
    0.25,  # delay between printing cycles
    bTerminate,  # bus to watch for termination signal
    "Print raw and derived data",  # Name of printer
    "Data bus readings are: ")  # Prefix for output

# Make a timer (a special kind of producer) that turns on the termination
# bus when it triggers
terminationTimer = rr.Timer(
    bTerminate,  # Output data bus
    10,  # Duration
    0.01,  # Delay between checking for termination time
    bTerminate,  # Bus to check for termination signal
    "Termination timer")  # Name of this timer

""" Fifth Part: Concurrent execution """

# Create a list of producer-consumers to execute concurrently
producer_consumer_list = [readPins,
                          interpretData,
                          controlServo,
                          printBuses,
                          terminationTimer]

# Execute the list of producer-consumers concurrently
rr.runConcurrently(producer_consumer_list)