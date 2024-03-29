import time
from picarx_improved import Picarx
import atexit

try:
    from robot_hat import ADC   
except ImportError:
    from sim_robot_hat import ADC

px = Picarx()

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
      
    def read(self):
        return self.get_grayscale_data()

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

class Controller():
    def __init__(self,scaling=1.0):
        self.scaling = scaling

    def control(self, value):

        if value == 0:
            px.set_dir_servo_angle(0)
            
        # elif value == 0.5: 
        #     px.set_dir_servo_angle(15*self.scaling)
            
        elif value == 1:
            px.set_dir_servo_angle(30*self.scaling)

        # elif value == -0.5:
        #     px.set_dir_servo_angle(-15*self.scaling)

        elif value == -1:
            px.set_dir_servo_angle(-30*self.scaling)


if __name__ == "__main__":
    sensor = Sensing()
    interpreter = Interpreter(sensitivity=0.95, polarity=-1) #light line (-1) , dark line (1)
    try:
        while True:
            px.forward(35)
            controller=Controller(scaling=1)
            controller.control(interpreter.map_readings_to_value(interpreter.interpret(sensor.read())))
            print(sensor.read())
            print(interpreter.interpret(sensor.read()))
            print(interpreter.map_readings_to_value(interpreter.interpret(sensor.read())))
            time.sleep(0.005) 
    except KeyboardInterrupt:
        px.stop()