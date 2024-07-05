# main.py
from vs_edit import main
from stepper_multi import xyz
from click_photo import capture_image

def pixels_to_mm(center_x_list, center_y_list):
    # Conversion factors based on image size and real-world coverage
    x_conversion_factor = 870 / 640  # mm per pixel for x-axis
    y_conversion_factor = 640 / 480  # mm per pixel for y-axis

    center_x_mm = [x * x_conversion_factor for x in center_x_list]
    center_y_mm = [y * y_conversion_factor for y in center_y_list]

    return center_x_mm, center_y_mm

def run_program():
    # Call the capture_image function to click and save the photo
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