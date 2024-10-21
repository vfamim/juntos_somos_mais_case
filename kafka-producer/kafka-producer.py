import time
import random
from confluent_kafka import Producer
import uuid
from faker import Faker
import json
import os

fake = Faker("en_GB")


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


# Producer configuration
producer_conf = {
    "bootstrap.servers": os.environ["BOOTSTRAP_SERVERS"],
    "security.protocol": "SASL_SSL",
    "sasl.mechanisms": "PLAIN",
    "sasl.username": os.environ["SASL_USERNAME"],
    "sasl.password": os.environ["SASL_PASSWORD"],
}


def generate_unique_id():
    return int(str(uuid.uuid4().int)[:8])


producer = Producer(producer_conf)


def generate_initial_data(transaction_id):
    date = fake.date_this_year()  # Random date within this year
    product_no = random.randint(10000, 999999)  # Product number between 5-6 digits
    product_name = fake.word().capitalize()  # Random product name
    price = round(random.uniform(5.0, 100.0), 2)  # Price in GBP
    quantity = random.randint(1, 5)  # Quantity of product
    customer_no = random.randint(10000, 99999)  # Customer number (5 digits)
    country = fake.country()  # Country name

    transaction_type = (
        "C" if random.random() < 0.1 else ""
    )  # 10% chance for cancelled transaction

    data = {
        "TransactionNo": f"{transaction_id}{transaction_type}",
        "Date": date,
        "ProductNo": product_no,
        "Product": product_name,
        "Price": price,
        "Quantity": quantity,
        "CustomerNo": customer_no,
        "Country": country,
    }

    if transaction_type == "C":
        data["Quantity"] = -quantity  # Negative quantity for cancelled transactions

    return data


if __name__ == "__main__":
    producer_id = generate_unique_id()
    initial_data = generate_initial_data(producer_id)

    while True:
        # Generate data for a transaction
        transaction_data = initial_data.copy()

        # Produce message to Kafka
        producer.produce(
            "time_pedido",
            key=str(producer_id),
            value=json.dumps(transaction_data),
            callback=delivery_report,
        )
        producer.poll(1)

        # Wait for 5 seconds before generating the next transaction
        time.sleep(5)
