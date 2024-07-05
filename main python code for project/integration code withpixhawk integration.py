import time
import os
from pymavlink import mavutil
from vs_edit import main
from stepper_multi import xyz
from click_photo import capture_image
import pixhawk

def pixels_to_mm(center_x_list, center_y_list):
    # Conversion factors based on image size and real-world coverage
    x_conversion_factor = 870 / 640  # mm per pixel for x-axis
    y_conversion_factor = 640 / 480  # mm per pixel for y-axis

    center_x_mm = [x * x_conversion_factor for x in center_x_list]
    center_y_mm = [y * y_conversion_factor for y in center_y_list]

    return center_x_mm, center_y_mm
def run_program():
    # Connect to the Pixhawk
    device_path = '/dev/ttymxc2'  # Serial port path
    master = pixhawk.connect_pixhawk(device_path)
    print("Connected to Pixhawk.")

    # Set the mode to GUIDED
    pixhawk.arm_and_guided_mode(master)

    # Read the waypoint file
    waypoint_file = "/home/mendel/new/farm_test.waypoints"  # Waypoint file location
    waypoints = pixhawk.read_waypoints(waypoint_file)
    print("Waypoints read from file.")

    for index, (serial_number, lat, lon) in enumerate(waypoints, start=1):
        # Send waypoint to the Pixhawk
        pixhawk.send_waypoint(master, index, lat, lon, True)
        print(f"Sent waypoint {index}: {lat}, {lon}")

        # Check if rover has reached the waypoint
        while not pixhawk.check_waypoint_reached(master, lat, lon):
            time.sleep(1)

        print(f"Rover reached waypoint {index}: {lat}, {lon}")

        # Disarm the motor
        pixhawk.toggle_motors(master, False)
        print("Motors disarmed.")

        # Capture image
        photo_captured = capture_image()
        if photo_captured:
            print("Image captured successfully.")
            # Call main() function
            center_x_list, center_y_list = main()
            center_x_mm, center_y_mm = pixels_to_mm(center_x_list, center_y_list)
            xyz(center_x_mm, center_y_mm)
            print("xyz() function completed.")
            # Arm the motor
            pixhawk.toggle_motors(master, True)
            print("Motors armed.")
        else:
            print("Error capturing photo. Skipping to the next waypoint.")

    # Disconnect from the Pixhawk
    pixhawk.disconnect_pixhawk(master)
    print("Disconnected from Pixhawk.")

if __name__ == "__main__":
    run_program()
