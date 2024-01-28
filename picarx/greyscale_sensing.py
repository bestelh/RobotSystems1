import time
from picarx_improved import Picarx

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
        # Assume readings is a list of three values
        avg = sum(readings) / len(readings)
        if self.polarity == 1:
            return [1 if (reading - avg) > self.sensitivity else 0 for reading in readings]
        else:
            return [0 if (reading - avg) > self.sensitivity else 1 for reading in readings]
            




if __name__ == "__main__":
    sensor = Sensing()
    interpreter = Interpreter(sensitivity=0.7, polarity=-1) #light line (-1) , dark line (1)
    #controller = Controller()
    while True:
        print(sensor.read())
        print(interpreter.interpret(sensor.read()))
        time.sleep(0.001)  # Wait for 0.1 seconds
        