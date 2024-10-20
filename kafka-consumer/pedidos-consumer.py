import json
import os
import time
from datetime import datetime

from kafka import KafkaConsumer

# Variáveis de ambiente para o Kafka
TOPIC = os.environ.get("TOPIC", "foobar")
CONSUMER_GROUP = os.environ.get("CONSUMER_GROUP", "cg-group-id")
BOOTSTRAP_SERVERS = os.environ.get(
    "BOOTSTRAP_SERVERS", "localhost:9091,localhost:9092,localhost:9093"
).split(",")

print("Iniciando consumidor...")


# Função para configurar o consumidor Kafka
def configurar_consumidor():
    try:
        consumidor = KafkaConsumer(
            TOPIC,
            bootstrap_servers=BOOTSTRAP_SERVERS,
            auto_offset_reset="latest",  # Consome as mensagens mais recentes
            enable_auto_commit=True,
            group_id=CONSUMER_GROUP,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        )
        return consumidor
    except Exception as e:
        if "NoBrokersAvailable" in str(e):
            print("Aguardando os brokers ficarem disponíveis")
        return "nao-disponivel"


# Função para calcular a diferença de tempo entre o recebimento da mensagem e o tempo atual
def diferenca_tempo(received_time):
    agora = int(datetime.now().strftime("%s"))
    return agora - received_time


# Loop para aguardar a disponibilidade dos brokers Kafka
print("Verificando se os brokers estão disponíveis...")
consumidor = "nao-disponivel"
while consumidor == "nao-disponivel":
    print("Brokers ainda não disponíveis...")
    time.sleep(5)
    consumidor = configurar_consumidor()

print("Brokers estão disponíveis e prontos para consumir mensagens")

# Loop para consumir e processar as mensagens recebidas
for mensagem in consumidor:
    try:
        dados_pedido = mensagem.value
        print(f"Pedido recebido:")
        print(f"  TransactionNo: {dados_pedido['TransactionNo']}")
        print(f"  Date: {dados_pedido['Date']}")
        print(f"  ProductNo: {dados_pedido['ProductNo']}")
        print(f"  Product: {dados_pedido['Product']}")
        print(f"  Price: £{dados_pedido['Price']}")
        print(f"  Quantity: {dados_pedido['Quantity']}")
        print(f"  CustomerNo: {dados_pedido['CustomerNo']}")
        print(f"  Country: {dados_pedido['Country']}")
        print("------------------------------------------------------")

    except Exception as e:
        print("Ocorreu uma exceção ao processar a mensagem")
        print(e)

# Fechar o consumidor Kafka
print("Fechando o consumidor")
consumidor.close()
