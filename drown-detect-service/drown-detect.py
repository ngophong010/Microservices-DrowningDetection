import cvlib as cv
from cvlib.object_detection import draw_bbox
import cv2
import time
import numpy as np
import sklearn
import joblib
import torch
import torch.nn as nn
import torch.nn.functional as F
import albumentations
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import argparse
import json
import os
import logging
from kafka import KafkaProducer
from datetime import datetime, timezone
import uuid
import pytz
from pytz import timezone

logging.basicConfig(level=logging.DEBUG)

# Kafka configurations
KAFKA_TOPIC = "drowning-alerts"
BOOTSTRAP_SERVER = os.getenv("KAFKA_BROKER", "kafka-local.drowning-detector.svc.cluster.local:9092")

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers = BOOTSTRAP_SERVER,
    value_serializer = lambda v: json.dumps(v).encode("utf-8"),
    security_protocol="SASL_PLAINTEXT",
    sasl_mechanism="SCRAM-SHA-256",
    sasl_plain_username="user1",
    sasl_plain_password="9WO6HhtXKB",

    # Add these parameters
    acks='all',
    retries=3,
    retry_backoff_ms=1000
)

# Send a message to Kafka
def send_drowning_alert():
    """
    Simulate the generation of a drowning detection alert message.
    """
    video_id = str(uuid.uuid4())
    timezone = pytz.timezone("Asia/Ho_Chi_Minh")
    message = {
        "video_id": video_id,
        "status": "drowning_detected",
        "timestamp": datetime.now(timezone).isoformat()  # Use the timezone properly
    }
    try:
    #     producer.send(KAFKA_TOPIC, message)
    #     # producer.flush()
    #     print(f"Alert sent: {message}")
    # except Exception as e:
    #     print(f"Failed to send alert: {e}")
        # Add delivery confirmation
        future = producer.send(KAFKA_TOPIC, message)
        record_metadata = future.get(timeout=10)
        print(f"Message sent successfully to topic {record_metadata.topic}")
        print(f"Partition: {record_metadata.partition}")
        print(f"Offset: {record_metadata.offset}")
    except Exception as e:
        print(f"Failed to send alert: {e}")
        # Add producer metrics
        metrics = producer.metrics()
        print(f"Producer metrics: {json.dumps(metrics, indent=2)}")

# Define command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--source', required=True, help='Video source file name')

# Parse command-line arguments
args = parser.parse_args()

print('Loading model and label binarizer...')
lb = joblib.load('lb.pkl')
class CustomCNN(nn.Module):
    def __init__(self):
        super(CustomCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 5)  # changed 3 to 1
        self.conv2 = nn.Conv2d(16, 32, 5)
        self.conv3 = nn.Conv2d(32, 64, 3)
        self.conv4 = nn.Conv2d(64, 128, 5)
        self.fc1 = nn.Linear(128, 256)
        self.fc2 = nn.Linear(256, len(lb.classes_))
        self.pool = nn.MaxPool2d(2, 2)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = self.pool(F.relu(self.conv4(x)))
        bs, _, _, _ = x.shape
        x = F.adaptive_avg_pool2d(x, 1).reshape(bs, -1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# lb = joblib.load('lb.pkl')
model = CustomCNN()
print('Model Loaded...')
model.load_state_dict(torch.load('model.pth', map_location='cpu'))
model.eval()
print('Loaded model state_dict...')

aug = albumentations.Compose([
    albumentations.Resize(224, 224),
    ])

def detectDrowning(source):
    isDrowning = False
    fram=0
    
    # Use video file name or camera source as the video_id
    video_id = os.path.basename(source) if not source.isdigit() else f"camera_{source}"

    #input from the camera
    if source.isdigit():
        cap = cv2.VideoCapture(int(source))  # for webcam input
    else:
        cap = cv2.VideoCapture("videos/" + source)  # for video file input

    if (cap.isOpened() == False):
        print('Error while trying to read video')

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    while(cap.isOpened()):
        status, frame = cap.read()

        # Apply object detection
        bbox, label, conf = cv.detect_common_objects(frame)
        
        # If only one person is detected, use model-based detection
        if len(bbox) == 1:
            bbox0 = bbox[0]
            #centre = np.zeros(s)
            centre = [0,0]

            for i in range(0, len(bbox)):
                centre[i] =[(bbox[i][0]+bbox[i][2])/2,(bbox[i][1]+bbox[i][3])/2 ]

            centre =[(bbox0[0]+bbox0[2])/2,(bbox0[1]+bbox0[3])/2 ]
            
            start_time = time.time()
            model.eval()
            with torch.no_grad():
                pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                pil_image = aug(image=np.array(pil_image))['image']
                if fram == 500:
                    break
                fram+=1
                pil_image = np.transpose(pil_image, (2, 0, 1)).astype(np.float32)
                pil_image = torch.tensor(pil_image, dtype=torch.float).cpu()
                pil_image = pil_image.unsqueeze(0)
                outputs = model(pil_image)
                _, preds = torch.max(outputs.data, 1)

            print("Swimming status : ",lb.classes_[preds])
            if(lb.classes_[preds] =='drowning'):
                isDrowning = True
                # Trigger Kafka alert
                send_drowning_alert()
                # Add this line to stop the video when drowning is detected in my case just break the loop, because I use input from .mp4 file
                cap.release()
            if(lb.classes_[preds] =='normal'):
                isDrowning = False
            out = draw_bbox(frame, bbox, label, conf, isDrowning)
            
        # if more than one person is detected, use logic-based detection
        elif len(bbox) > 1:
            # calculate the centroid of each bounding box
            centres = []
            for i in range(len(bbox)):
                bbox_i = bbox[i]
                centre_i = [(bbox_i[0] + bbox_i[2])/2, (bbox_i[1] + bbox_i[3])/2]
                centres.append(centre_i)
            
            # calculate the distance between each pair of centroids
            distances = []
            for i in range(len(centres)):
                for j in range(i+1, len(centres)):
                    dist = np.sqrt((centres[i][0] - centres[j][0])**2 + (centres[i][1] - centres[j][1])**2)
                    distances.append(dist)
            
            # if the minimum distance is less than a threshold, consider it as drowning
            if len(distances) > 0 and min(distances) < 50:
                isDrowning = True
            else:
                isDrowning = False
            out = draw_bbox(frame, bbox, label, conf, isDrowning)

        else:
            out = frame
            
        # display output, I containerize the app so I don't need to display the output
        # cv2.imshow("Real-time object detection", out)

        # press "Q" to stop
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     cap.release()
        #     cv2.destroyAllWindows()
        #     exit()
    
    cap.release()

detectDrowning(args.source)