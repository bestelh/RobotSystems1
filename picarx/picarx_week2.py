import atexit
import time
from picarx_improved import Picarx

def main():
    px = Picarx()
    atexit.register(px.stopping_motors)
    while True:
        command = input("Enter command: ") 
        # input_command= input("Enter Command (action angle speed time): " )
        # commands_to_array= input_command.split(" ")
        
        if  command.upper() == 'F':
            px.set_dir_servo_angle(int(input("Enter angle: ")))
            input_time= int(input("Run time (s): "))
            px.forward(int(input("Enter speed: ")))
            time.sleep(input_time)
            px.stop()

        elif command.upper() == 'B':
            px.set_dir_servo_angle(int(input("Enter angle: ")))
            px.backward(int(input("Enter speed: ")))
            time.sleep(int(input("Run time (s): ")))
            px.stop()

        elif command.upper() == 'E':
            px.stop()
            break

if __name__ == "__main__":
    main()