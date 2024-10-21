# Case Técnico Engenheiro de Dados -> Processamento de pedidos em Real Time

>"O objetivo desse case é criar um desenho de solução, com passo a passo para orientar um engenheiro de dados desenvolver uma solução de dados real time para a squad de pedidos. O resultado desse desenho deverá orientar as pessoas de dados e da squad com a solução. Esses documentos servirão como insumo para iniciar o desenvolvimento.
>A squad de produtos hoje conta com um(a) PM e pessoas de engenharia de software. Esse time fará parte da solução, criando o transacional da nossa solução de dados, portanto é necessário desenharmos a solução que contemple eles. Aqui é necessário sugerir uma arquitetura e ferramentas para a Squad, contextualizando tecnicamente e funcionalmente o time. A stack do lado de dados conta com um Databricks na Azure, mas ainda não tem uma solução para dados real time.
Os dados que receberemos estão nesse modelo ([https://www.kaggle.com/datasets/gabrielramos87/an-online-shop-business](https://www.kaggle.com/datasets/gabrielramos87/an-online-shop-business))
>É necessário também desenvolver um trecho de código para servir de exemplo para os engenheiros de software e de dados. Aqui, deixamos a sua escolha qual parte do código deseja construir para servir de exemplo. Podemos utilizar, Python, Pyspark, Sql e/ou Scala. Precisamos também explicar os motivadores para a escolha de tecnologia.
>Para documentar essa solução utilize uma ferramenta como [Draw.io](http://draw.io/), Miro ou excalidraw e para o código, utilize o github."

## Tecnologias Escolhidas

- [**Spark**](https://spark.apache.org/): É uma ferramenta para processar grandes volumes de dados de forma rápida, pois trabalha com dados em memória. Suporta várias linguagens e é ideal para análise de dados, machine learning e processamento em tempo real.

- [**Python**](https://www.python.org/): Uma linguagem de programação popular por ser simples e poderosa. Muito usada em ciência de dados, automação e machine learning, com várias bibliotecas que facilitam o trabalho com dados.

- [**Azure Databricks Notebook**](https://azure.microsoft.com/pt-br/products/databricks/): Uma interface interativa no Databricks (integrado com Azure) onde você pode rodar códigos (Python, SQL, etc.) em um ambiente colaborativo, ótimo para análise e ciência de dados.

- [**Airflow**](https://airflow.apache.org/): Plataforma para automatizar e gerenciar tarefas. Ele organiza fluxos de trabalho como um "passo a passo", ideal para programar e monitorar pipelines de dados.

- [**Docker**](https://www.docker.com/): Ferramenta que cria containers onde aplicativos rodam de forma isolada e consistente, independente do ambiente. Facilita desenvolvimento, testes e implantação de software.

- [**Confluent e Kafka**](https://www.confluent.io/): Kafka é uma ferramenta para lidar com grandes quantidades de dados em tempo real, como logs e eventos. Confluent é uma versão gerenciada do Kafka, com recursos extras para facilitar seu uso em empresas.

- [**Delta Live Tables**](https://learn.microsoft.com/en-us/azure/databricks/delta-live-tables/): Garante a qualidade dos dados automaticamente ao permitir que você defina regras de validação e acompanhe os dados em tempo real. Ele limpa, monitora e ajusta os dados durante o processamento, evitando problemas antes de chegarem às análises. 

- [**Azure Blob Storage**](https://azure.microsoft.com/en-us/products/storage/blobs): Serviço de armazenamento de alta performance, sendo excelente para criação de data lakehouse.

- [Power BI](https://app.powerbi.com/): Uma ferramenta para análise e visualização de dados, oferece diversos conectores e possui integração nativa com Azure.

## Diagrama


![image01](imgs/somosjuntosmais.jpeg)

## Arquitetura

Para a este projeto iremos implementar um **Data Lakehouse**. A ideia é termos uma arquitetura que une o melhor dos dois mundos: a flexibilidade de um **data lake** (onde você pode armazenar grandes volumes de dados brutos) e a estrutura organizada de um **data warehouse** (que facilita consultas rápidas e bem estruturadas) em uma estrutura chamada de "*Medalhão*", que se popularizou com o próprio **DataBricks**.
Um ponto importante para a escolha dessa arquitetura, é a probabilidade de podermos escalar futuramente para um **Data Mesh**, que é muito similar a um Data Lakehouse porém dividido em domínios, como: area de vendas, marketing, finanças, estratégia etc. 
Outra estratégia adotada é manter grande parte das ferramentas e serviços da Azure, uma vez que o time de dados atua com Azure Databricks, facilitando a integração e o escalonamento do projeto. 

## Processamento de pedidos

O **Apache Kafka**, facilita a ingestão de dados de pedidos em tempo real, a escolha do **Confluent** para esse projeto é a facilidade de uso, gerenciamento e escalabilidade de aplicações de streaming de dados em tempo real. Ela foi criada pelos fundadores do Kafka e conta com um grande arsenal e recursos que podem tornar todo o processamento de dados em algo mais robusto. Ele irá funcionar assim:

### Produtores ou Producers

Um produtor no Kafka é o componente responsável por enviar os dados de cada pedido para um **tópico** chamado `time_pedido`. Nesta etapa faremos a serialização das mensagens para o formato de JSON, largamente utilizado em projetos envolvendo dados em tempo real.
Esta etapa também ficará responsável pelo particionamento e monitoramento.

### Consumidores ou Consumers

Um consumidor no Kafka  é responsável pela leitura das mensagens de **tópicos** específicos. Aqui é o processo de deserialização, retornando os dados em um formato adequado para nosso data lakehouse.

## Database

### Camada Bronze (Raw Data)

Essa camada é armazenada no [Blob Storage](https://azure.microsoft.com/pt-br/products/storage/blobs/) e recebe os dados brutos diretamente das fontes, como logs de transações de vendas, interações de usuários no site e inventário de produtos. Os dados chegam de forma não processada, sem transformação, preservando o histórico completo e podendo conter inconsistências ou duplicidades. Seu objetivo é servir como um backup fiel da origem dos dados.

### Camada Silver (Cleaned Data)

Utilizando o [Delta Lake](https://learn.microsoft.com/en-us/azure/databricks/delta/) e [Delta Live Tables](https://docs.databricks.com/pt/delta-live-tables/index.html), a camada **Silver** aplica transformações iniciais nos dados da camada Bronze. Aqui, os dados são limpos, filtrados e padronizados para remover duplicatas e inconsistências. Essa camada traz os dados em um formato mais organizado e pronto para análise de operações diárias, como análises de comportamento de compra, tendências de vendas, e criação de relatórios operacionais. Ela mantém a granularidade dos dados, permitindo consultas mais rápidas.

### Camada Gold (Aggregated Data)

Na camada **Gold**, também baseada no [Delta Lake](https://learn.microsoft.com/en-us/azure/databricks/delta/) e [Delta Live Tables](https://docs.databricks.com/pt/delta-live-tables/index.html), os dados são otimizados e agregados para análise avançada e geração de insights estratégicos. Informações como relatórios financeiros, métricas de performance de vendas, análises de marketing e personalização de ofertas são derivadas desta camada. Ela oferece dados sumarizados e preparados para consumo por times de negócio ou modelos de machine learning, focando em performance e tomada de decisão.

## Orquestrador

A ferramenta escolhida para o orquestramento é o **Apache Airflow**, que gerencia workflows por meio de DAGs (Grafos Acíclicos Dirigidos) escritas em Python. Essas DAGs são facilmente escaláveis à medida que o volume de dados, tarefas e workflows cresce. Além disso, o Airflow oferece vantagens mesmo em soluções em tempo real, pois facilita o gerenciamento de dependências, permite configurar políticas de **retry** e agendamentos complexos, e integra-se facilmente com outras ferramentas, como **Databricks** e **Kafka**.

## Consumo de dados

Para o consumo dos dados desse projeto, ferramentas como o **Power BI**, que já possuem integração nativa com o **Azure**, são uma ótima escolha para análise e visualização em tempo real. O Power BI pode se conectar diretamente ao **Azure Data Lake**, **Azure Synapse Analytics**, ou **Delta Lake**, e permitir que você consuma os dados processados pela pipeline em tempo real ou com atualizações agendadas.

## Implementando o Projeto

### Dados

Nosso processamento se dará como base essa tabela com aqui:

| Campo             | Tipo      | Descrição                                                                                                   |
| ----------------- | --------- | ----------------------------------------------------------------------------------------------------------- |
| **TransactionNo** | Categoria | Um identificador único para cada transação. Se o código começar com "C", indica que o pedido foi cancelado. |
| **Date**          | String    | A data em que a transação foi registrada no sistema.                                                        |
| **ProductNo**     | Categoria | Código único de cinco ou seis dígitos usado para identificar um produto específico no sistema.              |
| **Product**       | Categoria | Nome do produto adquirido na transação.                                                                     |
| **Price**         | Numérico  | Valor unitário do produto em libras esterlinas (£), indicado para cada item comprado.                       |
| **Quantity**      | Numérico  | Número de unidades do produto compradas. Quantidades negativas representam transações canceladas.           |
| **CustomerNo**    | Categoria | Identificador único de cinco dígitos atribuído a cada cliente no sistema.                                   |
| **Country**       | Categoria | O país em que o cliente está localizado no momento da compra.                                               |

### Ingestão por Streaming

Para este projeto, o script escolhido foi a criação do Producer `kafka-producer.py` e Consumer  `kafka-consumer.py`, ambos os scripts utilizam a biblioteca do **Confluent**, sendo assim necessário a configuração de um ambiente para desenvolvimento. Para isso existe um guia para implementar algumas configurações necessárias neste arquivo aqui: [Confluent](./docs/01_configure_confluent_cli.md).

### Script Producer

Este código é um produtor Kafka que gera e envia mensagens de dados de transações para um tópico Kafka chamado `time_pedido`. Ele simula transações com detalhes gerados aleatoriamente, como número do produto, nome do produto, preço, quantidade, número do cliente e país, utilizando a biblioteca `Faker`. Um ID de transação único é atribuído a cada mensagem, e há uma chance de 10% de que a transação seja marcada como cancelada, indicada por quantidades negativas. Os dados são serializados em formato JSON e enviados para o Kafka. O produtor gera e envia continuamente uma nova transação a cada 5 segundos, e uma função de callback é usada para relatar o sucesso ou falha na entrega da mensagem.

### Script Consumer

Este código é um consumidor Kafka que lê mensagens de transações do tópico `transactions-topic`, processa essas mensagens em lotes e armazena os dados em uma tabela PostgreSQL chamada `time_pedido`. A cada mensagem consumida, os dados são desserializados de JSON, contendo campos como número da transação, data, número do produto, nome do produto, preço, quantidade, número do cliente e país. O consumidor acumula as mensagens e, quando atinge um lote de 100 mensagens ou um intervalo de 5 segundos, os dados são salvos no banco de dados usando o `pandas`. Ele continua consumindo mensagens indefinidamente até ser interrompido.

### Deploy

Para o deploy deste projeto basta utilizar preencher todas as variáveis de ambiente e executar o `docker-compose.yml`.
