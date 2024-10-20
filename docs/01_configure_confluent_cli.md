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
