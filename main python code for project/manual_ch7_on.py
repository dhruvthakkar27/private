import time
from pymavlink import mavutil
from yolo_detect import main
from click_photo import capture_image
from stepper_multi import xyz

# Connect to the autopilot
connection_string = '/dev/ttymxc2'

def pixels_to_mm(center_x_list, center_y_list):
    # Conversion factors based on image size and real-world coverage
    x_conversion_factor = 870 / 640  # mm per pixel for x-axis
    y_conversion_factor = 640 / 480  # mm per pixel for y-axis

    center_x_mm = [x * x_conversion_factor for x in center_x_list]
    center_y_mm = [y * y_conversion_factor for y in center_y_list]

    return center_x_mm, center_y_mm
try:
    # Establish the connection
    vehicle = mavutil.mavlink_connection(connection_string, baud=57600)

    # Wait for the heartbeat message to find the system ID
    vehicle.wait_heartbeat()
    print(f"Heartbeat from system (system {vehicle.target_system} component {vehicle.target_component})")

    

    def is_channel_7_on():
        # Request RC channels
        vehicle.mav.request_data_stream_send(
            vehicle.target_system,
            vehicle.target_component,
            mavutil.mavlink.MAV_DATA_STREAM_RC_CHANNELS,
            10,  # 10 Hz update rate
            1  # Start sending
        )
        
        # Wait for RC_CHANNELS message
        msg = vehicle.recv_match(type='RC_CHANNELS', blocking=True, timeout=1)
        
        if msg is None:
            print("No RC_CHANNELS message received")
            return False
        
        # Check if Channel 7 is high (usually > 1500 means 'on')
        return msg.chan7_raw >=1500

    print("Waiting for Channel 7 to be turned ON...")
    while True:
        if is_channel_7_on():
            print("Channel 7 is ON")
            print("Running object detection model...")
            
            # Capture image
            photo_captured = capture_image()

            if photo_captured:
                center_x_list, center_y_list = main()
                center_x_mm, center_y_mm = pixels_to_mm(center_x_list, center_y_list)
                xyz(center_x_mm, center_y_mm)
            else:
                print("Error capturing photo. Exiting program.")
            break
            
            
            
        
        time.sleep(0.1)  # Small delay to prevent CPU overuse

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the connection if it was established
    if 'vehicle' in locals() and hasattr(vehicle, 'close'):
        vehicle.close()
    print("Exiting...")