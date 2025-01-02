FROM python:3.9-slim

ENV KAFKA_BROKER="kafka-local.drowning-detector.svc.cluster.local:9092"

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN ls -la /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["python", "DrownAlerts.py"]
