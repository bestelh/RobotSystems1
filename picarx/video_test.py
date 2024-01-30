import cv2
import numpy as np
 
# Function to process the image and determine the line position

def process_image(image):

    # Convert the image to grayscale

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
    # Apply Gaussian blur to reduce noise and improve edge detection

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
 
    # Use Canny edge detection to find edges in the image

    edges = cv2.Canny(blurred, 50, 150)
 
    # Find contours in the edges

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
    if contours:

        # Get the largest contour (assuming it's the line)

        largest_contour = max(contours, key=cv2.contourArea)
 
        # Get the bounding box of the largest contour

        x, y, w, h = cv2.boundingRect(largest_contour)
 
        # Calculate the center of the line

        line_center = x + w // 2
 
        return line_center
 
    # If no contours are found, return None

    return None
 
# Function to control the robot based on the line position

def control_robot(line_center, image_width):

    if line_center is not None:

        # Calculate the deviation from the center

        deviation = line_center - image_width // 2
 
        # You can implement your own control logic here

        # For example, adjust the robot's motors based on the deviation

        # For simplicity, let's print the deviation

        print(f"Deviation: {deviation}")
 
# Main function to capture video and control the robot

def main():

    # Use the camera (0 indicates the default camera, adjust if necessary)

    cap = cv2.VideoCapture(0)
 
    while True:

        # Capture a frame

        ret, frame = cap.read()
 
        # Process the frame to find the line position

        line_center = process_image(frame)
 
        # Control the robot based on the line position

        control_robot(line_center, frame.shape[1])
 
        # Display the processed image

        cv2.imshow('Line Following', frame)
 
        # Exit the loop if 'q' key is pressed

        if cv2.waitKey(1) & 0xFF == ord('q'):

            break
 
    # Release the camera and close all OpenCV windows

    cap.release()

    cv2.destroyAllWindows()
 
if __name__ == "__main__":

    main()
