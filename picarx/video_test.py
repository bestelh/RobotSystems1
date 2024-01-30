import cv2
import numpy as np
from picarx_improved import Picarx

def process_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        line_center = x + w // 2
        
        # Draw a line on the image at the line center
        cv2.line(image, (line_center, 0), (line_center, image.shape[0]), (0, 255, 0), 2)
        return line_center
    
    return None
 
def control_robot(line_center, image_width):
    if line_center is not None:
        deviation = line_center - image_width // 2
        #print(f"Deviation: {deviation}")
 
def main():
    px = Picarx()
    cap = cv2.VideoCapture(0)
    # Set desired frame width and height
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    px.set_cam_tilt_angle(-45)
    while True:
        ret, frame = cap.read()
        line_center = process_image(frame)
        control_robot(line_center, frame.shape[1])
        cv2.imshow('Line Following', frame)
 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 
    cap.release()
    cv2.destroyAllWindows()
 
if __name__ == "__main__":
    main()
    
