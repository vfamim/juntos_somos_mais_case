from confluent_kafka import Producer

from psycopg2
import json
import os
import random
import time

from dotenv import load_dotenv

load_dotenv()


conf = {
    "bootstrap.servers": os.getenv("BOOTSTRAP_SERVERS"),
    "sasl.mechanisms": "PLAIN",
    "security.protocol": "SASL_SSL",
    "sasl.username": os.getenv("SASL_USERNAME"),
    "sasl.password": os.getenv("SASL_PASSWORD"),
    "client.id": os.getenv("CLIENT_ID"),
}

producer = Producer(**conf)


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


topic = os.getenv("TOPIC")

def get_data_from_postgres():
    try:
        conn = psycopg2.connect(
            dbname="seu_banco",
            user="seu_usuario",
            password="sua_senha",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        query = "SELECT id, nome, valor FROM sua_tabela"
        cursor.execute(query)

        rows = cursor.fetchall()
        return rows

    except Exception as e:
        print(f"Erro ao conectar no PostgreSQL: {e}")
        return []

def produce_data_to_kafka():
    data = get_data_from_postgres()

    for row in data:
        message = {
            'id': row[0],
            'nome': row[1],
            'valor': row[2]
        }

        producer.produce(
            'meu_topico',
            key=str(row[0]),
            value=json.dumps(message),
            callback=delivery_report
        )

        producer.poll(0)

    producer.flush()

if __name__ == "__main__":
    produce_data_to_kafka()
