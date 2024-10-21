FROM python:3.9-slim

WORKDIR /app

COPY kafka-consumer.py .

RUN pip install confluent_kafka sqlalchemy pandas psycopg2-binary

CMD ["python", "kafka-consumer.py"]
