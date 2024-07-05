import re
import cv2
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
    input_tensor[:, :] = np.expand_dims((image - 255) / 255, axis=0)

def get_output_tensor(interpreter, index):
    """Returns the output tensor at the given index."""
    output_details = interpreter.get_output_details()[index]
    tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
    return tensor

def compute_iou(box1, box2):
    """Computes the Intersection over Union (IoU) of two bounding boxes."""
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    xi1 = max(x1, x2)
    yi1 = max(y1, y2)
    xi2 = min(x1 + w1, x2 + w2)
    yi2 = min(y1 + h1, y2 + h2)

    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
    box1_area = w1 * h1
    box2_area = w2 * h2

    union_area = box1_area + box2_area - inter_area
    iou = inter_area / union_area

    return iou

def non_max_suppression(boxes, scores, iou_threshold):
    """Performs Non-Maximum Suppression (NMS) on the bounding boxes."""
    indices = np.argsort(scores)[::-1]

    keep = []
    while len(indices) > 0:
        current = indices[0]
        keep.append(current)
        if len(indices) == 1:
            break
        rest = indices[1:]

        remaining_boxes = [boxes[i] for i in rest]
        current_box = boxes[current]

        ious = np.array([compute_iou(current_box, box) for box in remaining_boxes])
        indices = indices[np.where(ious <= iou_threshold)[0] + 1]

    return keep

def detect_objects(interpreter, image, threshold):
    """Returns a list of detection results, each a dictionary of object info."""
    set_input_tensor(interpreter, image)
    interpreter.invoke()

    raw_output = get_output_tensor(interpreter, 0)  # Assuming the raw output is at index 0
    output = (raw_output.T)

    boxes_xywh = output[..., :4]  # First 4 columns are bounding box coordinates
    scores = np.max(output[..., 5:], axis=1)  # Maximum score value from the 5th column onwards
    classes = np.argmax(output[..., 5:], axis=1)  # Class with the highest score from the 5th column onwards

    results = []
    boxes = []
    confidences = []

    num_detections = boxes_xywh.shape[0]
    for i in range(num_detections):
        if scores[i] >= threshold:
            x_center, y_center, width, height = boxes_xywh[i]
            xmin = int(max(1, (x_center - width / 2) * CAMERA_WIDTH))
            ymin = int(max(1, (y_center - height / 2) * CAMERA_HEIGHT))
            xmax = int(min(CAMERA_WIDTH, (x_center + width / 2) * CAMERA_WIDTH))
            ymax = int(min(CAMERA_HEIGHT, (y_center + height / 2) * CAMERA_HEIGHT))

            boxes.append([xmin, ymin, xmax - xmin, ymax - ymin])
            confidences.append(scores[i])

            result = {
                'bounding_box': [xmin, ymin, xmax, ymax],
                'class_id': classes[i],
                'score': scores[i]
            }
            results.append(result)

    # Apply Non-Maximum Suppression
    indices = non_max_suppression(boxes, confidences, iou_threshold=0.5)

    # Filter the results using the NMS indices
    nms_results = [results[i] for i in indices]

    return nms_results

def main():
    labels = load_labels()
    interpreter = tflite.Interpreter('yolo.tflite', experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])
    interpreter.allocate_tensors()
    _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']
    print("Model input shape:", input_height, input_width)

    img_1 = cv2.imread('1.jpg')
    print("Image loaded")
    img = cv2.resize(cv2.cvtColor(img_1, cv2.COLOR_BGR2RGB), (input_width, input_height))
    print("Image converted and resized")
    
    res = detect_objects(interpreter, img, 0.5)
    print("Detection results:", res)
    
    center_x_list = []
    center_y_list = []

    for result in res:
        xmin, ymin, xmax, ymax = result['bounding_box']

        cv2.rectangle(img_1, (xmin, ymin), (xmax, ymax), (0, 255, 0), 3)
        cv2.putText(img_1, labels[int(result['class_id'])], (xmin, min(ymax, CAMERA_HEIGHT - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        center_x = int((xmin + xmax) / 2)
        center_y = int((ymin + ymax) / 2)
        print("x =", center_x, ", y =", center_y)
        cv2.circle(img_1, (center_x, center_y), 5, (0, 0, 255), -1)
        center_x_list.append(center_x)
        center_y_list.append(center_y)
    
    print("center x list:", center_x_list)
    print("center y list:", center_y_list)

    cv2.imwrite('2.jpg', img_1)
    print("Image saved as 2.jpg")

    if cv2.waitKey(10) & 0xFF == ord('q'):
        cv2.destroyAllWindows()

    start_time = time.time()
    interpreter.invoke()
    stop_time = time.time()
    print('Time taken for inference: {:.3f}ms'.format((stop_time - start_time) * 1000))
    return center_x_list, center_y_list

if __name__ == "__main__":
    center_x_list, center_y_list = main()
