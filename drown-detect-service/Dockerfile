# Base image with Python
FROM python:3.9-slim

# Set environment variables to prevent Python output buffering and .pyc generation
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
ENV QT_QPA_PLATFORM=offscreen
ENV OPENCV_VIDEOIO_PRIORITY=5000
# Set environment variables (e.g. for KAFKA_BROKER and any other config you need)
ENV KAFKA_BROKER="kafka-local.drowning-detector.svc.cluster.local:9092"

# Install system dependencies for OpenCV and other tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libssl-dev \
    libx11-xcb1 \
    libxcb-render0 \
    libxcb-shm0 \
    libxcb-xfixes0 \
    libxcb1 \
    qtbase5-dev \
    qtchooser \
    qt5-qmake \
    qtbase5-dev-tools \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
    
# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt ./

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the application source code
COPY . ./

# Debugging step: List files in the /app directory to ensure correct copying
RUN ls -la /app

# Command to run your Python script to process `.mp4` files
ENTRYPOINT ["python", "/app/drown-detect.py"]

# Allow arguments to be passed for video source
CMD ["--source", "drowning_001.mp4"]
