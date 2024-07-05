
import re
import cv2
from tflite_runtime.interpreter import Interpreter
import numpy as np
import tflite_runtime.interpreter as tflite
import time

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

def load_labels(path='labels.txt'):
  """Loads the labels file. Supports files with or without index numbers."""
  with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    labels = {}
    for row_number, content in enumerate(lines):
      pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
      if len(pair) == 2 and pair[0].strip().isdigit():
        labels[int(pair[0])] = pair[1].strip()
      else:
        labels[row_number] = pair[0].strip()
  return labels

def set_input_tensor(interpreter, image):
  """Sets the input tensor."""
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = np.expand_dims((image-255)/255, axis=0)


def get_output_tensor(interpreter, index):
  """Returns the output tensor at the given index."""
  output_details = interpreter.get_output_details()[index]
  tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
  return tensor


def detect_objects(interpreter, image, threshold):
    """Returns a list of detection results, each a dictionary of object info."""
    set_input_tensor(interpreter, image)
    interpreter.invoke()
    # Get all output details
    boxes = get_output_tensor(interpreter, 1)
    print("boxes:",boxes)
    classes = get_output_tensor(interpreter, 3)
    print("classes:",classes)
    scores = get_output_tensor(interpreter, 0)
    print("scores:",scores)
    count_array = get_output_tensor(interpreter, 2)  # Get the count array

    print("count_array:", count_array)  # Print the count array

    # Use the count from the first element of count_array
 

    results = []
    # Verify the shape of scores
    if len(scores.shape) > 0:
        num_detections = scores.shape[0]
        for i in range(num_detections):
            if i < num_detections:
                if scores[i] >= threshold:
                    result = {
                        'bounding_box': boxes[i],
                        'class_id': classes[i],
                        'score': scores[i]
                    }
                    results.append(result)
            else:
                print("Index out of bounds or empty arrays detected.")
    else:
        print("Scores array is empty or has invalid shape.")

    return results    
def main():
    labels = load_labels()
    interpreter = tflite.Interpreter('yolo.tflite',experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])
    interpreter.allocate_tensors()
    _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']
    print("inte: ",input_height,input_width)

    img_1=cv2.imread('5.jpg')
   # cv2.imshow('input img',img_1)
    print("img loaded")
    img = cv2.resize(cv2.cvtColor(img_1, cv2.COLOR_BGR2RGB), (640,640))
   # cv2.imshow('converted',img)
    print("converted")
    res = detect_objects(interpreter, img, 0.5)
    print(res)
    center_x_list=[]
    center_y_list=[]
    for result in res:
      ymin, xmin, ymax, xmax = result['bounding_box']
      xmin = int(max(1,xmin * CAMERA_WIDTH))
      xmax = int(min(CAMERA_WIDTH, xmax * CAMERA_WIDTH))
      ymin = int(max(1, ymin * CAMERA_HEIGHT))
      ymax = int(min(CAMERA_HEIGHT, ymax * CAMERA_HEIGHT))

      cv2.rectangle(img_1,(xmin, ymin),(xmax, ymax),(0,255,0),3)
      cv2.putText(img_1,labels[int(result['class_id'])],(xmin, min(ymax, CAMERA_HEIGHT-20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2,cv2.LINE_AA) 
      center_x = int((xmin + xmax) / 2)
      center_y = int((ymin + ymax) / 2)
      print("x =",center_x,", y =",center_y)
      cv2.circle(img_1, (center_x, center_y), 5, (0, 0, 255), -1)
      center_x_list.append(center_x)
      center_y_list.append(center_y)
      print("center x list: ",center_x_list)
      print("center y list: ",center_y_list)    
     # cv2.imshow('Pi Feed', img_1)
    cv2.imwrite('2.jpg',img_1)
   
    if cv2.waitKey(10) & 0xFF ==ord('q'):
       cv2.destroyAllWindows()
    start_time = time.time()
    interpreter.invoke()
    stop_time = time.time()
    print('time: {:.3f}ms'.format((stop_time - start_time) * 1000))
    return center_x_list, center_y_list
if __name__ == "__main__":
    center_x_list, center_y_list = main()

