import cv2

def open_live_feed():
    # Open the default camera
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened correctly
    if not cap.isOpened():
        print("Error opening camera")
        return

    # Get the frame dimensions
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Live feed resolution: {width} x {height} pixels")

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame was captured correctly
        if not ret:
            print("Error capturing frame")
            break

        # Display the resulting frame
        cv2.imshow('Live Feed', frame)

        # Wait for the 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Call the open_live_feed function
open_live_feed()