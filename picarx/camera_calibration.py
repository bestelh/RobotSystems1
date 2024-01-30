import time
from picarx_improved import Picarx

def main():
    px = Picarx()
    px.set_cam_tilt_angle(int(input("Enter angle: ")))


if __name__ == "__main__":
    main()