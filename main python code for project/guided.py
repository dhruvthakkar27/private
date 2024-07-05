import time
from pymavlink import mavutil
from armmodecheck import arm_vehicle

def change_mode_to_guided(master, guided_mode=15):
    """
    Changes the vehicle's mode to GUIDED.

    Args:
        master (mavutil.mavlink_connection): The MAVLink connection to the vehicle.
        guided_mode (int): The mode identifier for GUIDED mode (default is 15).

    Returns:
        bool: True if the mode change is confirmed, False otherwise.
    """
    print("Attempting to set mode to GUIDED...")
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        guided_mode, 0, 0, 0, 0, 0
    )

    # Start time for timeout
    start_time = time.time()

    # Listen for COMMAND_ACK and check the response
    while time.time() - start_time < 10:  # Timeout after 10 seconds
        ack_msg = master.recv_match(type='COMMAND_ACK', blocking=True, timeout=1)
        if ack_msg:
            print("Received ACK for command: {}, result: {}".format(ack_msg.command, ack_msg.result))
            if ack_msg.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
                print("Command accepted by the vehicle. Checking mode persistence...")
                # Confirm mode change
                for i in range(10):  # Confirm over several heartbeats
                    msg = master.recv_match(type='HEARTBEAT', blocking=True, timeout=1)
                    if msg and msg.custom_mode == guided_mode:
                        print("GUIDED mode confirmed persistently.")
                        return True
                    elif msg:
                        print("Current mode still not GUIDED, current mode:", msg.custom_mode)
                        time.sleep(1)
                else:
                    print("Failed to confirm GUIDED mode after multiple checks.")
            else:
                print("Command was not accepted by the vehicle. Result code:", ack_msg.result)
            return False
        else:
            print("No acknowledgment received, command may not have been received.")

    print("Timeout reached. Failed to set mode to GUIDED.")
    return False

# Example of setting up a MAVLink connection and using the function
if __name__  == "__main__":
    print("we are in")
    master = mavutil.mavlink_connection('/dev/ttymxc2', baud=57600)
    master.wait_heartbeat()
    print("Heartbeat received from system (system %u component %u)" % (master.target_system, master.target_component))

    # Change mode to GUIDED
    result = change_mode_to_guided(master)
    arm_vehicle(master)
    if result:
        print("Mode successfully changed to GUIDED.")
    else:
        print("Failed to change mode to GUIDED.")
