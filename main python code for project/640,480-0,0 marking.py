import cv2

def capture_image_and_mark_coordinates():
    # Open the default camera
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened correctly
    if not cap.isOpened():
        print("Error opening camera")
        return

    # Capture a single frame
    ret, frame = cap.read()

    # Check if the frame was captured correctly
    if not ret:
        print("Error capturing frame")
        cap.release()
        return

    # Get the dimensions of the frame
    height, width, _ = frame.shape

    # Mark the (0, 0) and (640, 480) pixel coordinates
    frame = cv2.circle(frame, (0, 0), 5, (0, 0, 255), -1)  # Red dot at (0, 0)
    frame = cv2.circle(frame, (640, 480), 5, (0, 255, 0), -1)  # Red dot at (640, 480)

    # Save the captured frame as "marked_image.jpg"
    cv2.imwrite("marked_image.jpg", frame)

    # Release the camera
    cap.release()

    # Display the marked image
    marked_image = cv2.imread("marked_image.jpg")
    cv2.imshow("Marked Image", marked_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("Image with marked coordinates saved as marked_image.jpg")

# Call the capture_image_and_mark_coordinates function
capture_image_and_mark_coordinates()