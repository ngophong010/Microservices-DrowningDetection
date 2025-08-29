# # Base image with Python
# FROM python:3.12-slim

# # Set the working directory in the container
# WORKDIR /app

# # Install system dependencies (e.g., for OpenCV, if needed)
# RUN apt-get update && apt-get install -y \
#     libgl1-mesa-glx \
#     && rm -rf /var/lib/apt/lists/*

# # Copy the requirements file to the container
# COPY requirements.txt ./

# # Install the required Python packages
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy all the application source code
# COPY drown-detect.py .
# # Copy the cvlib directory with object_detection.py
# COPY cvlib/ cvliv/   
# COPY cvlib/data/ data/

# # Copy Kafka client configuration
# COPY client.properties /etc/kafka/client.properties

# # Debugging step: List files in the /app directory to ensure correct copying
# RUN ls -la /app

# COPY client.properties /etc/kafka/client.properties

# # Set environment variables (optional, can be overridden by Helm)
# ENV KAFKA_BROKER=kafka-local:9092
# ENV VIDEO_FILE="drowning_001.mp4"

# # Command to run your Python script to process `.mp4` files
# # ENTRYPOINT ["python", "/app/drown-detect.py"]

# # Allow arguments to be passed for video source
# CMD ["python", "drown-detect.py", "--source", "$VIDEO_FILE"]

# ---- Builder Stage ----
# Use a full Python image to install dependencies
FROM python:3.9-slim as builder

WORKDIR /usr/src/app

# Install poetry or pip
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels -r requirements.txt

# ---- Final Stage ----
# Use a minimal base image for the final product
FROM python:3.9-slim

WORKDIR /usr/src/app

# Copy the pre-built wheels from the builder stage
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .

# Install dependencies from local wheels to avoid redownloading
RUN pip install --no-cache /wheels/*

# Copy application code
COPY . .

# Expose port and run the application
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
