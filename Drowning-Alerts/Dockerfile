# Use a slim Python base image to minimize the image size
FROM python:3.9-slim

# Set environment variables (e.g. for KAFKA_BROKER and any other config you need)
ENV KAFKA_BROKER="kafka-local.drowning-detector.svc.cluster.local:9092"

# Set a working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt ./

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory's contents into the container's working directory
COPY . /app

# Debugging step: List files in the /app directory to ensure correct copying
RUN ls -la /app

# Install dependencies from your requirements.txt file
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Command to run your script (make sure the script runs on container start)
CMD ["python", "DrownAlerts.py"]
