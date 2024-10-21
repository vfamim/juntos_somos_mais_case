import time
import random
from confluent_kafka import Consumer, KafkaError
import json
import os
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# Consumer configuration
consumer_conf = {
    "bootstrap.servers": os.environ["BOOTSTRAP_SERVERS"],
    "security.protocol": "SASL_SSL",
    "sasl.mechanisms": "PLAIN",
    "sasl.username": os.environ["SASL_USERNAME"],
    "sasl.password": os.environ["SASL_PASSWORD"],
    "group.id": "transactions-consumer-group",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(consumer_conf)
consumer.subscribe(["transactions-topic"])

# PostgreSQL configuration
db_url = f"{os.environ['DB_URL']}"
engine = create_engine(db_url)


def consume_messages():
    batch_size = 100  # Number of messages to process per batch
    batch_interval = 5  # Time interval (in seconds) between batches
    messages = []
    start_time = time.time()  # Initialize start_time inside the function

    try:
        while True:
            msg = consumer.poll(1.0)  # Wait for up to 1 second for a new message
            if msg is None:
                continue
            if msg.error():
                continue

            value = json.loads(
                msg.value().decode("utf-8")
            )  # Decode the message value to JSON
            # Denormalize the message
            data = {
                "TransactionNo": value["TransactionNo"],
                "Date": value["Date"],
                "ProductNo": value["ProductNo"],
                "Product": value["Product"],
                "Price": value["Price"],
                "Quantity": value["Quantity"],
                "CustomerNo": value["CustomerNo"],
                "Country": value["Country"],
                "Time": datetime.now(),  # Capture the current timestamp of the message
            }
            messages.append(data)

            # Process the batch when it reaches the size or the time interval
            if (
                len(messages) >= batch_size
                or (time.time() - start_time) >= batch_interval
            ):
                df = pd.DataFrame(messages)
                df.to_sql("transaction_data", engine, if_exists="append", index=False)
                messages = []  # Clear the message list after saving to the database
                start_time = time.time()  # Reset the time counter

    except KeyboardInterrupt:
        pass
    finally:
        print("Closing consumer.")
        consumer.close()


if __name__ == "__main__":
    start_time = time.time()
    consume_messages()
