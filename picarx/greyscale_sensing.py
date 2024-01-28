import time
from picarx_improved import Picarx

try:
    from robot_hat import ADC   
except ImportError:
    from sim_robot_hat import ADC

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

if __name__ == "__main__":
    sensor1 = Sensing()
    while True:
        print(sensor1.read())
        time.sleep(0.1)  # Wait for 0.1 seconds
        