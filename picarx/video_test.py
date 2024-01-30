import cv2
import numpy as np
from picarx_improved import Picarx
import time

def process_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
        
        # Draw a circle on the image at the center of the largest contour
        cv2.circle(gray, (cX, cY), 5, (255), -1)
        return (cX, cY), gray
    
    return None, gray

def control_robot(center, image_width):
    if center is not None:
        cX, cY = center
        deviation = cX - image_width // 2
        # Calculate the deviation as a proportion of the image width
        deviation_proportion = deviation / image_width
        # Convert the deviation proportion to a turning angle
        # The maximum turning angle is assumed to be 45 degrees
        turning_angle = deviation_proportion * 30
        return turning_angle
    return None
 
def main():
    px = Picarx()
    cap = cv2.VideoCapture(0)
    # Set desired frame width and height
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    px.set_cam_tilt_angle(-45)
    while True:
        #px.forward(50)
        ret, frame = cap.read()
        line_center, processed_image = process_image(frame)
        turning_angle = control_robot(line_center, frame.shape[1])
        if turning_angle is not None:
            # Use the turning angle to control the robot
            # The control function is assumed to take a turning angle in degrees
            px.set_dir_servo_angle(turning_angle)
        cv2.imshow('Line Following', processed_image)
 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    time.sleep(0.1)
    cap.release()
    cv2.destroyAllWindows()
 
if __name__ == "__main__":
    main()