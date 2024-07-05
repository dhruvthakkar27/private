# main.py
from vs_edit import main
from stepper_multi import xyz
from click_photo import capture_image
from guide import change_mode_to_guided
from pixhawk import connect_pixhawk 
from pixhawk import toggle_motors
from pixhawk import send_waypoint
from pixhawk import check_waypoint_reached
from pixhawk import read_waypoints
master = '/dev/ttymxc2'
connect_pixhawk(master)
lat, lon = read_waypoints("/home/mendel/new/test.waypoint")

def pixels_to_mm(center_x_list, center_y_list):
    # Conversion factors based on image size and real-world coverage
    x_conversion_factor = 870 / 640  # mm per pixel for x-axis
    y_conversion_factor = 640 / 480  # mm per pixel for y-axis

    center_x_mm = [x * x_conversion_factor for x in center_x_list]
    center_y_mm = [y * y_conversion_factor for y in center_y_list]

    return center_x_mm, center_y_mm


def run_program():
    
    
    # Call the capture_image function to click and save the photo
    
    print(lat)
    print(lon)
    toggle_motors(master,True)
    change_mode_to_guided(master)
    #ack_msg = master.recv_match(type='COMMAND_ACK', blocking=True, timeout=10)
   # Assuming `master` is the MAVLink connection and `guided_mode` is the desired mode identifier for GUIDED mode

# while True:
#     ack_msg = master.recv_match(type='COMMAND_ACK', blocking=True, timeout=10)  # Wait for COMMAND_ACK message
#     if ack_msg:
#         print("Received ACK for command: {}, result: {}".format(ack_msg.command, ack_msg.result))
#         if ack_msg.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
#             print("Command accepted by the vehicle. Checking mode persistence...")
#             # Confirm mode change
#             for i in range(10):  # Confirm over several heartbeats
#                 msg = master.recv_match(type='HEARTBEAT', blocking=True, timeout=5)
#                 if msg and msg.custom_mode == guided_mode:
#                     print("GUIDED mode confirmed persistently.")
#                     break  # Exit the loop once GUIDED mode is confirmed
#                 elif msg:
#                     print("Current mode still not GUIDED, current mode:", msg.custom_mode)
#                     time.sleep(1)
#             else:
#                 print("Failed to confirm GUIDED mode after multiple checks.")
#         else:
#             print("Command was not accepted by the vehicle. Result code:", ack_msg.result)
#     else:
#         print("No acknowledgment received, command may not have been received.")
    
#     # If GUIDED mode is confirmed, break out of the loop
#     if msg and msg.custom_mode == guided_mode:
#         break


send_waypoint(master, lat, lon)
check_waypoint_reached(master, lat, lon)
# Assuming `master` is the MAVLink connection and `lat` and `lon` are the waypoint coordinates

while True:
    # Check if waypoint is reached
    if check_waypoint_reached(master, lat, lon):
        # Waypoint reached, turn off the motor
        toggle_motors(master, enable=False)
        print("Waypoint reached. Motor turned off.")
        break  # Exit the loop once waypoint is reached
    else:
        # Waypoint not reached yet, continue monitoring
        pass


photo_captured = capture_image()

    # Check if the photo was captured successfully
if photo_captured:
        # Call the main() function from vs_edit.py
    center_x_list, center_y_list = main()

        # Convert pixel coordinates to millimeter coordinates
    center_x_mm, center_y_mm = pixels_to_mm(center_x_list, center_y_list)

        # Call the xyz function from stepper_multi.py, passing the millimeter lists as arguments
    xyz(center_x_mm, center_y_mm)
else:
    print("Error capturing photo. Exiting program.")

if __name__ == "__main__":
    run_program()