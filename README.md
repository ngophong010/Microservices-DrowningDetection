# Drwoning-Detector


Introducing our drowning detection system, designed to detect and alert when someone is in danger of drowning.
Our system uses computer vision algorithms to analyze video feeds from multiple cameras around a pool or other bodies of water.

The system works by using a deep learning-based object detection model to identify a person in the water. The model is trained on thousands of images and videos of people in water environments, allowing it to accurately recognize a human body in a variety of positions and lighting conditions. Once a person is detected, the system uses motion analysis algorithms to track their movements and monitor their safety.

Overall, the drowning detection system provides an innovative and effective solution for ensuring the safety of people in and around swimming pools. By leveraging advanced computer vision and machine learning technologies, the system can quickly and accurately identify potential drowning incidents and alert caregivers, ultimately helping to save lives.

## Installation

To set up the Drowning Detection project, follow these steps:

1. **Clone the Project:** (With Test Sample Videos):
```bash   
   git clone https://github.com/randhana/Drowning-Detection-.git
```
    **Clone the Project:** Without Test Sample Videos - Lightweight Version
```bash
   git clone --branch lightweight https://github.com/randhana/Drowning-Detection-.git
```
2. **Create a Virtual Environment:**
```bash
  python -m venv env
```
3. **Install Requirements:**
```bash
   pip install -r requirements.txt
```

# Usage

To run the program, follow these steps:

1. **Create a "videos" Folder:**
    - Inside the project folder, create a new folder called "videos."

2. **Add Sample Videos:**
    - Place sample videos into the "videos" folder.

3. **Run the Program:**
```bash
python DrownDetect.py --source video_file_name.mp4
```

5. To quit the program, press the "q" key on your keyboard.

[Here's](https://youtu.be/99GdhIozAQ8) a demonstration video of our drowning detection system in action

If you are interested in YOLO object detection, read their website:

https://pjreddie.com/darknet/yolo/


THIS IS FOR PYTHON KAFKA KUBERNETES MICROSERVICE ARCHITECTURE
### Install kafka
```shell
helm repo add bitnami https://charts.bitnami.com/bitnami

helm install kafka-local bitnami/kafka \
--set persistence.enabled=false,zookeeper.persistence.enabled=false

kubectl run kafka-local-client \
    --restart='Never' \
    --image docker.io/bitnami/kafka:3.3.1-debian-11-r19 \
    --namespace drown-detector-microservice \
    --command \
    -- sleep infinity

kubectl exec --tty -i kafka-local-client --namespace drown-detector-microservice -- bash
```
### Commands
```shell
# Drowning Detect service
kubectl run drown-detect-svc --rm --tty -i \
    --image phongngolam/drown-detect-service  \
    --restart Never \
    --namespace drown-detector-microservice
    
# Drowning alert service
kubectl run drown-alert-svc --rm --tty -i \
    --image phongngolam/drown-alert-service \
    --restart Never \
    --namespace drown-detector-microservice

### Kafka UI
```shell
helm repo add kafka-ui https://provectus.github.io/kafka-ui
helm install kafka-ui kafka-ui/kafka-ui \
--set envs.config.KAFKA_CLUSTERS_0_NAME=kafka-local \
--set envs.config.KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=kafka-local.drown-detector-microservice.svc.cluster.local:9092

kubectl port-forward svc/kafka-ui 8080:8080
```