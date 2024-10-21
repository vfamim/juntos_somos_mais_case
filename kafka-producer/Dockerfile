FROM python:3.9-slim

WORKDIR /app

COPY kafka-producer.py .

RUN pip install faker confluent_kafka

CMD ["python", "kafka-producer.py"]
