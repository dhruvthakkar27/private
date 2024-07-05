import os
import random
import shutil

def split_train_test(directory, train_ratio=0.8):
    # Get list of all files in the directory
    files = os.listdir(directory)
    # Filter out only image files
    image_files = [f for f in files if f.lower().endswith('.jpg')]

    # Shuffle the list of image filenames
    random.shuffle(image_files)

    # Calculate the number of images for training and testing
    num_train = int(len(image_files) * train_ratio)
    num_test = len(image_files) - num_train

    # Create train and test directories if they don't exist
    train_dir = r"D:\TFOD\TFODCourse\Tensorflow\workspace\images\train"
    test_dir = r"D:\TFOD\TFODCourse\Tensorflow\workspace\images\test"
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Move images and corresponding XML files to train and test directories
    for i, filename in enumerate(image_files):
        src_image_path = os.path.join(directory, filename)
        src_xml_path = os.path.join(directory, filename[:-4] + '.xml')  # Assuming XML files have the same name as images but with .xml extension
        if i < num_train:
            dest_image_path = os.path.join(train_dir, filename)
            dest_xml_path = os.path.join(train_dir, filename[:-4] + '.xml')
        else:
            dest_image_path = os.path.join(test_dir, filename)
            dest_xml_path = os.path.join(test_dir, filename[:-4] + '.xml')
        shutil.move(src_image_path, dest_image_path)
        shutil.move(src_xml_path, dest_xml_path)
        print(f"Moved {filename} and its corresponding XML file to {'train' if i < num_train else 'test'} directory")

if __name__ == "__main__":
    directory = r"D:\dataset-for-Weed\9-5-2024"
    split_train_test(directory)
