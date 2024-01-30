import cv2
import numpy as np
from picarx_improved import Picarx
import time

def process_image(image):
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
    if contours:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]
        centers = []
        for contour in contours:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                centers.append((cX, cY))
        
        if len(centers) == 2:
            middle_point = ((centers[0][0] + centers[1][0]) // 2, (centers[0][1] + centers[1][1]) // 2)
            
            # Create a separate color image for drawing
            drawing_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            # Draw a red circle at the middle point
            cv2.circle(drawing_image, (middle_point[0], middle_point[1]), 5, (0, 0, 255), -1)
            # Draw a line from the bottom middle of the screen to the middle point
            cv2.line(drawing_image, (width // 2, height), (middle_point[0], middle_point[1]), (0, 0, 255), 2)
            return (middle_point[0] + width*2//6, middle_point[1] + height*5//6), drawing_image
    
    return None, cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

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