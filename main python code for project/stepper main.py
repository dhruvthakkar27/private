from periphery import GPIO
from time import sleep
import multiprocessing

# Constants for X axis
RESOLUTION_X = 1600  # steps per revolution
BALL_SCREW_PITCH_X = 10  # in mm per rotation for X axis
MAX_LENGTH_X = 790  # Maximum length for X axis

# Constants for Y axis
RESOLUTION_Y = 1600  # steps per revolution
BALL_SCREW_PITCH_Y = 5  # in mm per rotation for Y axis
MAX_LENGTH_Y = 790  # Maximum length for Y axis

# Declare clockwise and counter-clockwise direction variables
cw_direction = True
ccw_direction = False

# Function to calculate steps from millimeters for X axis
def mm_to_steps_x(distance_mm):
    # Limit the input distance to the maximum length for X axis
    distance_mm = min(distance_mm, MAX_LENGTH_X)
    # Calculate number of rotations needed for X axis
    rotations = distance_mm / BALL_SCREW_PITCH_X
    # Calculate total steps for X axis
    total_steps = rotations * RESOLUTION_X
    return int(total_steps)

# Function to calculate steps from millimeters for Y axis
def mm_to_steps_y(distance_mm):
    # Limit the input distance to the maximum length for Y axis
    distance_mm = min(distance_mm, MAX_LENGTH_Y)
    # Calculate number of rotations needed for Y axis
    rotations = distance_mm / BALL_SCREW_PITCH_Y
    # Calculate total steps for Y axis
    total_steps = rotations * RESOLUTION_Y
    return int(total_steps)

# Function to move a single axis
def move_axis(steps, direction_gpio, pulse_gpio):
    direction = cw_direction if steps >= 0 else ccw_direction
    direction_gpio.write(bool(direction))

    for _ in range(abs(int(steps))):
        pulse_gpio.write(True)
        sleep(0.001)
        pulse_gpio.write(False)
        sleep(0.0005)

# Function to run the X axis movement
def run_step_x(steps_x, gpio_direction_x, gpio_pulse_x):
    move_axis(steps_x, gpio_direction_x, gpio_pulse_x)

# Function to run the Y axis movement
def run_step_y(steps_y, gpio_direction_y, gpio_pulse_y):
    move_axis(steps_y, gpio_direction_y, gpio_pulse_y)

# Function to handle the coordinate list
def xyz(center_list_x, center_list_y):
    x1 = 0
    y1 = 0
    center_list_x.append(0)
    center_list_y.append(0)
    print("center_list_x", center_list_x)
    print("center_list_y", center_list_y)

    # Open GPIO pin for relay control
    laser = GPIO("/dev/gpiochip4", 12, "out")

    for i in range(len(center_list_x)):
        x2 = center_list_x[i]
        y2 = center_list_y[i]
        dist_x = x2 - x1
        dist_y = y2 - y1
        main(dist_x, dist_y)
        x1 = x2
        y1 = y2
    
    if i != len(center_list_x) - 1:
        # Turn on the GPIO pin for relay control
        print("i", i)
        laser.write(False)
        print("laser on")
        sleep(2)
        # Turn off the GPIO pin for relay control
        laser.write(True)
        print("laser off")
    else:
        # Last element, assume home position is reached
        laser.write(True)
        print("home pos reached")

# Clean up GPIO pin for relay control
    laser.close()

# Main function for both axes movement
def main(x_distance_mm, y_distance_mm):
    # Calculate steps for X axis
    steps_x = mm_to_steps_x(x_distance_mm)
    # Calculate steps for Y axis
    steps_y = mm_to_steps_y(y_distance_mm)

    # Open GPIO pins for both axes
    gpio_direction_x = GPIO("/dev/gpiochip4", 10, "out") #pin18
    gpio_pulse_x = GPIO("/dev/gpiochip2", 9, "out")#pin16 gnd pin 14
    gpio_direction_y = GPIO("/dev/gpiochip4", 13, "out")#pin36
    gpio_pulse_y = GPIO("/dev/gpiochip2", 13, "out")#pin37 gnd pin 39

    try:
        # Move both axes simultaneously
        print('Moving both axes...')

        # Create two separate processes
        process_x = multiprocessing.Process(target=run_step_x, args=(steps_x, gpio_direction_x, gpio_pulse_x))
        process_y = multiprocessing.Process(target=run_step_y, args=(steps_y, gpio_direction_y, gpio_pulse_y))

        # Start the processes
        process_x.start()
        process_y.start()

        # Wait for the processes to finish
        process_x.join()
        process_y.join()

        print('Movement completed.')

    except KeyboardInterrupt:
        # Clean up GPIO pins for both axes
        gpio_direction_x.close()
        gpio_pulse_x.close()
        gpio_direction_y.close()
        gpio_pulse_y.close()

# Example usage in your main code
if __name__ == "__main__":
    # Example: Define the list of coordinates
    center_list_x = [10, 20, 30, 40]
    center_list_y = [50, 60, 70, 80]

    xyz(center_list_x, center_list_y)