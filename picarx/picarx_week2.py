import atexit
import time
from picarx_improved import Picarx

def main():
    px = Picarx()
    atexit.register(px.stopping_motors)
    while True:
        command = input("Enter command (F,B,3PT,PR,PL): ") 
        # input_command= input("Enter Command (action angle speed time): " )
        # commands_to_array= input_command.split(" ")3pt
        
        if  command.upper() == 'F':
            px.set_dir_servo_angle(int(input("Enter angle: ")))
            input_time= int(input("Run time (s): "))
            px.forward(int(input("Enter speed: ")))
            time.sleep(input_time)
            px.stop()

        elif command.upper() == 'B':
            px.set_dir_servo_angle(int(input("Enter angle: ")))
            input_time= int(input("Run time (s): "))
            px.backward(int(input("Enter speed: ")))
            time.sleep(input_time)
            px.stop()

        elif command.upper() == '3PT':
            px.set_dir_servo_angle(10)
            px.forward(90)
            time.sleep(2)
            px.set_dir_servo_angle(-25)
            px.backward(90)

            time.sleep(2)
            px.set_dir_servo_angle(0)
            px.forward(90)
            time.sleep(1)
            px.stop()

        elif command.upper() == 'PR':
            px.set_dir_servo_angle(30)
            px.backward(80)
            time.sleep(1)

            px.set_dir_servo_angle(-30)
            px.backward(80)
            time.sleep(1.25)

            px.set_dir_servo_angle(0)
            px.forward(70)
            time.sleep(0.35)
            px.stop()

        elif command.upper() == 'PL':
            px.set_dir_servo_angle(-30)
            px.backward(80)
            time.sleep(1)

            px.set_dir_servo_angle(30)
            px.backward(80)
            time.sleep(1.25)

            px.set_dir_servo_angle(0)
            px.forward(70)
            time.sleep(0.35)
            px.stop()

        elif command.upper() == 'E':
            px.stop()
            break

if __name__ == "__main__":
    main()