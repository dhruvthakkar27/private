import os
import pymavlink
from pymavlink import mavutil
import math
# Connect to the Pixhawk over UART
def connect_pixhawk(device_path):
    master = mavutil.mavlink_connection(device_path, baud=57600)
    master.wait_heartbeat()
    print("Connected to Pixhawk")
    return master

# Disconnect from the Pixhawk
def disconnect_pixhawk(master):
    master.mav.mission_ack_send(mavutil.mavlink.MAV_MISSION_TYPE_MISSION, 0, mavutil.mavlink.MAV_MISSION_ACCEPTED)
    master.close()
    print("Disconnected from Pixhawk")

def arm_and_guided_mode(master):
    # Set guided mode
    mode_id = mavutil.mavlink.MAV_MODE_GUIDED_ARMED  # Mode ID for guided armed mode
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE,
        0,
        mode_id,
        0, 0, 0, 0, 0, 0
    )
    print("Rover armed and in guided mode")

# Read waypoints from a file
def read_waypoints(file_path):
    lat = []
    lon = []
    with open(file_path, 'r') as file:
        for line in file:
            fields = line.strip().split()
            if len(fields) >= 9:  # Check if the line has at least 9 fields
                waypoint_number = int(fields[0])
                latitude = float(fields[8])
                longitude = float(fields[9])
                lat.append(latitude)
                lon.append(longitude)
    return lat, lon


# Send a waypoint to the Pixhawk
def send_waypoint(master, lat, lon):
    target_coordinate_mask = 0b0000111111111000
    velocity_ignore_mask = 0b0000000000001000
    altitude = 1

    # Convert latitude and longitude to integers
    lat_int = int(lat * 1e7)
    lon_int = int(lon * 1e7)

    # Establish MAVLink connection
    master = mavutil.mavlink_connection('/dev/ttymxc2', baud=57600)
    master.wait_heartbeat()
    print("Connected to Pixhawk")

    # Encode and send MAVLink message
    msg = master.mav.set_position_target_global_int_encode(
        master.target_system,
        master.target_component,
        0,  # Time boot ms (not used)
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
        target_coordinate_mask,
        lat_int,  # Latitude (scaled to 1e7)
        lon_int,  # Longitude (scaled to 1e7)
        altitude,  # Altitude (meters)
        0, 0, 0,  # Velocity components (not used)
        0, 0, 0,  # Acceleration components (not used)
        0, 0
    )

    # Send the MAVLink message
    master.mav.send(msg)

    
  
        


def check_waypoint_reached(master, lat, lon):
    while True:
        msg = master.recv_match(type=['GLOBAL_POSITION_INT'], blocking=True)  # Wait for the GLOBAL_POSITION_INT message
        if msg:
            current_lat = msg.lat / 1e7
            current_lon = msg.lon / 1e7
            distance_to_waypoint = distance_between_points(current_lat, current_lon, lat, lon)
            return distance_to_waypoint < 1  # Adjust the radius as needed

def distance_between_points(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on Earth using Haversine formula.
    """
    R = 6371000  # Earth radius in meters

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) * math.sin(delta_phi / 2) + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2) * math.sin(delta_lambda / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


# Function to toggle the motor state
def toggle_motors(master, enable):
    master = mavutil.mavlink_connection(device_path, baud=57600)
    master.wait_heartbeat()
    print("Connected to Pixhawk")
    if enable:
        print("Enabling motors")
        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            1, 0, 0, 0, 0, 0, 0
        )
    else:
        print("Disabling motors")
        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            0, 0, 0, 0, 0, 0, 0
        )

