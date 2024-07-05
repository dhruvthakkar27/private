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
    for i in range(len(lat)):
        lat_value = lat[i]
        lon_value = lon[i]
        print("Waypoint:", lat_value, lon_value)
        toggle_motors(master, True)
        #change_mode_to_guided(master) beacause we want to drive in manual 
        send_waypoint(master, lat_value, lon_value)  # Pass single values as lists
        check_waypoint_reached(master, lat_value, lon_value)
        
        while not check_waypoint_reached(master, lat_value, lon_value):
            pass  # Wait until waypoint is reached
        
        toggle_motors(master, enable=False)
        print("Waypoint reached. Motor turned off.")
        
        photo_captured = capture_image()

        if photo_captured:
            center_x_list, center_y_list = main()
            center_x_mm, center_y_mm = pixels_to_mm(center_x_list, center_y_list)
            xyz(center_x_mm, center_y_mm)
        else:
            print("Error capturing photo. Exiting program.")
            break



if __name__ == "__main__":
    run_program()
