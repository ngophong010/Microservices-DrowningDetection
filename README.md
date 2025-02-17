# 🔥 Drowning Detection - Enhanced Version
This project is based on Drowning-Detection and has been improved for better compatibility, performance, and deployment on Kubernetes.

## 🚀 Key Modifications
- Updated Dependencies: Adjusted requirements.txt for compatibility with Python 3.12.
- Microservices Enhancement: Optimized for deployment in a Kubernetes environment.
- Improved Logging & Debugging: Enhanced logging for better observability.
- Performance Tweaks: Refactored some parts to improve efficiency.

## 📌 Original Repository
The original project was created by @randhana(https://github.com/randhana), and you can find it here:
🔗 Drowning-Detection on GitHub(https://github.com/randhana/Drowning-Detection-)

## Overview
Introducing our drowning detection system, designed to detect and alert when someone is in danger of drowning.
Our system uses computer vision algorithms to analyze video feeds from multiple cameras around a pool or other bodies of water.

The system works by using a deep learning-based object detection model to identify a person in the water. The model is trained on thousands of images and videos of people in water environments, allowing it to accurately recognize a human body in a variety of positions and lighting conditions. Once a person is detected, the system uses motion analysis algorithms to track their movements and monitor their safety.

Overall, the drowning detection system provides an innovative and effective solution for ensuring the safety of people in and around swimming pools. By leveraging advanced computer vision and machine learning technologies, the system can quickly and accurately identify potential drowning incidents and alert caregivers, ultimately helping to save lives.

### Key Features:
- **Computer Vision Algorithms:** Analyze video feeds from multiple cameras.
- **Deep Learning Model:** Trained on thousands of images to detect human bodies in various positions and lighting conditions.
- **Motion Analysis:** Tracks movements to assess potential danger.

By providing rapid and accurate detection, this system helps to save lives and improve pool safety.


## Installation

Follow the steps below to set up the Drowning Detection system:

### Clone the Project
#### Clone with Test Sample Videos
```bash
git clone https://github.com/randhana/Drowning-Detection-.git
```

#### Clone Without Test Sample Videos (Lightweight Version)
```bash
git clone --branch lightweight https://github.com/randhana/Drowning-Detection-.git
```

#### Clone the Microservices Version of My Drowning Detection Project
```bash
git clone https://github.com/ngophong010/Microservices-DrowningDetection.git
```

### Create a Virtual Environment
```bash
python -m venv env
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

To run the Drowning Detection program, follow these steps:

1. **Create a "videos" Folder:**
   - Inside the project directory, create a folder named `videos`.

2. **Add Sample Videos:**
   - Place video files into the `videos` folder.

3. **Run the Program:**
```bash
python DrownDetect.py --source video_file_name.mp4
```

4. **Quit the Program:**
   - Press the `q` key on your keyboard.

[Watch our demonstration video](https://youtu.be/99GdhIozAQ8) showcasing the drowning detection system in action.

### Additional Resources

For more details on YOLO object detection, visit their [official website](https://pjreddie.com/darknet/yolo/).

## Microservices Architecture

This project uses Python, Kafka, Kubernetes, and a microservices-based architecture. Below are the instructions for setting up and deploying related components.

### Install Kafka
1. Add the Bitnami Helm repository:
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
```

2. Install Kafka without persistence:
```bash
helm install kafka-local bitnami/kafka --set persistence.enabled=false,zookeeper.persistence.enabled=false
```

3. Deploy a Kafka client pod:
```bash
kubectl run kafka-local-client --restart='Never' --image docker.io/bitnami/kafka:3.3.1-debian-11-r19 \
--namespace drown-detector-microservice --command -- sleep infinity
```

4. **Retrieve Kafka Client Password:**
   - Run the following command to retrieve the password for the Kafka client:
     ```bash
     kubectl get secret kafka-local-user-passwords --namespace drown-detector-microservice -o jsonpath='{.data.client-passwords}' | base64 -d
     ```
   - Note the password as you will need it for authentication.

5. **Create a `client.properties` File:**
   - Inside your local environment, create a file named `client.properties` with the following content:
     ```
     security.protocol=SASL_PLAINTEXT
     sasl.mechanism=SCRAM-SHA-256
     sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
         username="user1" \
         password="<retrieved_password>";
     ```
   - Replace `<retrieved_password>` with the actual password you retrieved in the previous step.

6. **Copy the `client.properties` File to the Kafka Client Pod:**
```bash
kubectl cp --namespace drown-detector-microservice ./client.properties kafka-local-client:/tmp/client.properties
```

7. If you want to access the Kafka client:
```bash
kubectl exec --tty -i kafka-local-client --namespace drown-detector-microservice -- bash
```

### Deploy Services
#### Drowning Detect Service
```bash
kubectl run drown-detect-svc --rm --tty -i --image phongngolam/drown-detect-service --restart Never --namespace drown-detector-microservice
```
 
#### Drowning Alert Service
```bash
kubectl run drown-alert-svc --rm --tty -i --image phongngolam/drown-alert-service --restart Never --namespace drown-detector-microservice
```

### Kafka UI
1. Add the Kafka UI Helm repository:
```bash
helm repo add kafka-ui https://provectus.github.io/kafka-ui
```

2. Install Kafka UI:
```bash
helm install kafka-ui kafka-ui/kafka-ui \
--set envs.config.KAFKA_CLUSTERS_0_NAME=kafka-local \
--set envs.config.KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=kafka-local.drown-detector-microservice.svc.cluster.local:9092
```

3. Access the Kafka UI via port forwarding:
```bash
kubectl port-forward svc/kafka-ui 8080:8080
```


