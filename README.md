# Case Técnico Engenheiro de Dados -> Juntos Somos Mais

Este projeto foi desenvolvido para a empresa **JUNTOS SOMOS MAIS** e visa implementar um fluxo de dados em tempo real utilizando o **Confluent**, **Apache Kafka** e **Python**. O projeto realiza a leitura de dados de uma tabela chamada **E-commerce Business Transaction** e processa esses dados em real-time.

## Contexto

- **Objetivo**
  - Criar um **desenho de solução** com um passo a passo para orientar um engenheiro de dados no desenvolvimento de uma solução de dados em tempo real para a squad de pedidos.
  - O resultado do desenho deverá orientar tanto as pessoas de dados quanto a squad de pedidos.

- **Documentação:**
  - Os documentos gerados servirão como **insumo** para iniciar o desenvolvimento da solução.

- **Equipe envolvida:**
  - A squad de produtos
  - A equipe de engenharia de software

- **Arquitetura e ferramentas:**
  - Sugerir uma **arquitetura** e ferramentas para a squad de pedidos.
  - O desenho da solução precisa **contextualizar tecnicamente e funcionalmente** o time.
  - A stack de dados utiliza o **Databricks** na Azure, mas ainda não há uma solução para dados em tempo real.

- **Dados a serem utilizados:**
  - O modelo de dados que será utilizado está disponível em: [Kaggle Dataset - Online Shop Business](https://www.kaggle.com/datasets/gabrielramos87/an-online-shop-business).

- **Exemplo de código:**
  - Desenvolver um **trecho de código** de exemplo para os engenheiros de software e de dados.
  - Pode-se utilizar **Python, PySpark, SQL** ou **Scala**.
  - A escolha da tecnologia deve ser justificada com base em **motivadores técnicos**.

- **Ferramentas para documentação:**
  - Para documentar a solução, utilizar ferramentas como **Draw.io**, **Miro** ou **Excalidraw**.
  - O código deve ser disponibilizado no **GitHub**.

- **Prazos e entrega:**
  - O prazo para realizar o case é de **5 dias**, com entrega até **16 de outubro**.
  - O resultado deverá ser enviado respondendo ao e-mail original.

- **Encerramento:**
  - A mensagem é finalizada com um agradecimento pelo contato anterior.

## Requisitos

Antes de começar, você precisará instalar e configurar os seguintes componentes:

- **Confluent CLI** para gerenciar o cluster Confluent Cloud
- **Python 3.x**
- Bibliotecas Python necessárias (veja abaixo como instalar)
- Uma conta no **Confluent Cloud** ou um ambiente local do Confluent

## Configurando o Confluent CLI

### 1. Instale o Confluent CLI

Baixe e instale o Confluent CLI seguindo as instruções da [documentação oficial](https://docs.confluent.io/confluent-cli/current/install.html).

### 2. Faça login no Confluent Cloud

Se você estiver usando o Confluent Cloud, faça o login com o comando:

```bash
confluent login
```

Siga as instruções na tela para autenticar com suas credenciais.

### 3. Crie um Cluster Kafka

Após fazer login, você pode criar um cluster Kafka no Confluent Cloud ou usar um já existente. Para criar um novo cluster:

```bash
confluent kafka cluster create ecommerce-cluster --cloud aws --region us-east-1
```

Ou liste seus clusters existentes:

```bash
confluent kafka cluster list
```

### 4. Configure o Cluster

Depois de criar ou identificar seu cluster, defina-o como o cluster ativo:

```bash
confluent kafka cluster use <cluster-id>
```

### 5. Crie um Tópico Kafka

Crie um tópico Kafka para transmitir as transações de e-commerce:

```bash
confluent kafka topic create ecommerce-transactions
```

Você pode verificar se o tópico foi criado com sucesso usando:

```bash
confluent kafka topic list
```

### 6. Configuração da API Key

Para se conectar ao cluster Kafka usando seus scripts Python, você precisará de uma **API Key** e **Secret**:

```bash
confluent api-key create --resource <cluster-id>
```

Guarde a chave e o segredo fornecidos, pois serão necessários para configurar os Producers e Consumers.

## Estrutura do Projeto

O projeto contém dois scripts principais para o Kafka Producer e o Kafka Consumer.

### 1. **Kafka Producer** (`producer.py`)

Este script é responsável por enviar dados da tabela **E-commerce Business Transaction** para o tópico Kafka em tempo real.

#### Exemplo de execução do `producer.py`:

```bash
python producer.py
```

### 2. **Kafka Consumer** (`consumer.py`)

O script do Consumer consome os dados do tópico Kafka e realiza o processamento necessário.

#### Exemplo de execução do `consumer.py`:

```bash
python consumer.py
```

## Configuração dos Scripts Python

### Instalação das Dependências

No diretório do projeto, instale as dependências Python utilizando o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Dependências principais:**

- `confluent-kafka`
- `json`
- `time`

### Configurando `producer.py`

No script `producer.py`, você precisará ajustar as configurações do Kafka Producer, incluindo as chaves de API e o endereço do cluster Kafka.

Exemplo de trecho de código no `producer.py`:

```python
from confluent_kafka import Producer
import json

config = {
    'bootstrap.servers': '<bootstrap-server>',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': '<api-key>',
    'sasl.password': '<api-secret>',
}

producer = Producer(config)
topic = 'ecommerce-transactions'

def delivery_report(err, msg):
    if err is not None:
        print(f'Error: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

# Exemplo de envio de mensagem
transaction = {"order_id": "12345", "amount": 250, "status": "completed"}
producer.produce(topic, key=str(transaction["order_id"]), value=json.dumps(transaction), callback=delivery_report)
producer.flush()
```

### Configurando `consumer.py`

No script `consumer.py`, ajuste as configurações do Kafka Consumer da mesma forma, utilizando as chaves de API e o endereço do cluster.

Exemplo de trecho de código no `consumer.py`:

```python
from confluent_kafka import Consumer, KafkaError

config = {
    'bootstrap.servers': '<bootstrap-server>',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': '<api-key>',
    'sasl.password': '<api-secret>',
    'group.id': 'ecommerce-consumer-group',
    'auto.offset.reset': 'earliest',
}

consumer = Consumer(config)
topic = 'ecommerce-transactions'
consumer.subscribe([topic])

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break
    print(f'Received message: {msg.value().decode("utf-8")}')
consumer.close()
```

## Executando o Projeto

1. **Inicie o Kafka Producer**:
   - O Producer lê os dados da tabela "E-commerce Business Transaction" e os envia para o tópico Kafka.
   - Execute o script `producer.py`.

2. **Inicie o Kafka Consumer**:
   - O Consumer consome os dados do tópico Kafka e processa os dados em real-time.
   - Execute o script `consumer.py`.

## Conclusão

Este projeto demonstra como configurar um pipeline de dados em real-time utilizando **Confluent**, **Apache Kafka** e **Python**, focando na transmissão de dados da tabela **E-commerce Business Transaction**. A flexibilidade do Kafka permite que você escale e processe eventos de maneira eficiente em diversas situações de negócios.

---

Se precisar de mais detalhes ou ajustes específicos, me avise!
