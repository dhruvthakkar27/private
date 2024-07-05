import cv2
import os
from datetime import datetime

def capture_and_save_photo(output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get current timestamp for unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Open default camera (usually webcam)
    cap = cv2.VideoCapture(0)
    
    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    # Capture a frame
    ret, frame = cap.read()
    
    # Check if frame was captured successfully
    if not ret:
        print("Error: Could not capture frame.")
        return
    
    # Generate unique filename
    filename = os.path.join(output_dir, f"photo_{timestamp}.jpg")
    
    # Save the captured frame as an image
    cv2.imwrite(filename, frame)
    
    # Release the camera
    cap.release()
    
    print(f"Photo captured and saved as: {filename}")

# Example usage:
output_directory = "D:\dataset-for-Weed\9-5-2024"
capture_and_save_photo(output_directory)