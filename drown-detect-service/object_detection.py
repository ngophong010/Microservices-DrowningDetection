import cv2
from ultralytics import YOLO

COLORS = [(0, 255, 0), (0, 255, 0), (255, 255, 255)]
model = YOLO('yolov8n.pt')

def draw_bbox(img, bbox, labels, confidence, Drowning, write_conf=False):
    for i, label in enumerate(labels):
        if label == 'person' and Drowning:
            color = COLORS[1]
            label = 'ALERT DROWNING'
        else:
            color = COLORS[0]
            label = 'Normal'
        if write_conf:
            label += ' ' + str(format(confidence[i] * 100, '.2f')) + '%'
        cv2.rectangle(img, (bbox[i][0], bbox[i][1]), (bbox[i][2], bbox[i][3]), color, 2)
        cv2.putText(img, label, (bbox[i][0], bbox[i][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return img

def detect_common_objects(image, confidence=0.5, nms_thresh=0.3):
    if image is None:
        return [], [], []
    results = model(image)
    bbox, label, conf = [], [], []
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf_score = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            if conf_score > confidence and class_name == 'person':
                bbox.append([x1, y1, x2, y2])
                label.append(class_name)
                conf.append(conf_score)
    return bbox, label, conf