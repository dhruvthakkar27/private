import time
from pymavlink import mavutil

# Serial port path and baud rate
serial_port = '/dev/ttymxc2'
baud_rate = 57600

try:
    # Establish the serial connection
    master = mavutil.mavlink_connection(serial_port, baud=baud_rate)
    print(f"Connected to serial port: {serial_port}")
except Exception as e:
    print(f"Error connecting to serial port: {e}")
    print("Not connected")
    exit()

# Request the heartbeat message
master.mav.request_data_stream_send(master.target_system, master.target_component, mavutil.mavlink.MAV_DATA_STREAM_ALL, 10, 1)

# Wait for the heartbeat message
while True:
    msg = master.recv_match(type='HEARTBEAT', blocking=True)
    if msg is not None:
        print(f"Received heartbeat message: {msg}")
        break

# Close the serial connection
master.close()