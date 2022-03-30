# Kafka Setup - Local
- Run zookeeper service

  ```
  zookeeper-server-start.bat ..\..\config\zookeeper-properties.props
  ```

- Run Kafka server

  ```
  kafka-server-start.bat ..\..\config\server.props
  ```

# Flask API - Publisher endpoints for kafka and pubsub

Server runs here and produces messages

  ```
  py app.py
  ```

- To publish a message to kafka message queue

  ```
  http://localhost:5000/kafka/push-to-consumer?start_idx=0&end_idx=1
  ```

- To publish a message to pubsub message queue

  ```
  http://localhost:5000/pubsub/push-to-consumer?start_idx=0&end_idx=1
  ```

Here, start_idx and end_idx represent the test set index for fashion MNIST dataset.

The above endpoints are called when user submits the form displayed on root url.

# Kafka Consumer
- Consumer with model inference lives here

  ```
  py consumer.py
  ```

- Output is the list of predicted class labels on the test set based on the start_idx and end_idx provided
- Output is printed to consumer console

# Google Pubsub Subscriber
- Subscriber with model inference lives here

  ```
  py subscriber.py
  ```

- Output is the list of predicted class labels on the test set based on the start_idx and end_idx provided
- Output is printed to subscriber console

# Setup Instructions

## Kafka Setup
- https://www.geeksforgeeks.org/how-to-install-and-run-apache-kafka-on-windows/
- https://www.youtube.com/watch?v=EUzH9khPYgs

## Pubsub Setup
- https://cloud.google.com/pubsub/docs/create-topic-gcloud
- https://cloud.google.com/pubsub/docs/create-topic-console
- Credential file must be placed at root

# Model
- CNN based mode on on Fashion MNIST Dataset.
- To train/update model, update the `fashion_mnist_model.ipynb` notebook.

# Requirements
```
pip install -r requirements.txt
```

# References
- https://cloud.google.com/pubsub/docs/emulator
- https://cloud.google.com/pubsub/docs/create-topic-console
- https://cloud.google.com/pubsub/docs/publisher
- https://github.com/googleapis/python-pubsub/blob/main/samples/snippets/subscriber.py
