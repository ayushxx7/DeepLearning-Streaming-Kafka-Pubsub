# Kafka Setup - Local
1. Run zookeeper service

```
zookeeper-server-start.bat ..\..\config\zookeeper-properties.props
```

2. Run Kafka server

```
kafka-server-start.bat ..\..\config\server.props
```

# Flask API - Publisher endpoints for kafka and pubsub
3. server runs here and produces messages

```
py app.py
```

# Kafka Consumer
4. consumer with model inference lives here

```
py consumer.py
```

# Google Pubsub Subscriber
5. subscriber with model inference lives here

```
py subscriber.py
```

### Kafka Setup
- https://www.geeksforgeeks.org/how-to-install-and-run-apache-kafka-on-windows/
- https://www.youtube.com/watch?v=EUzH9khPYgs

### Pubsub Setup
- https://cloud.google.com/pubsub/docs/create-topic-gcloud
- https://cloud.google.com/pubsub/docs/create-topic-console
- Credential file must be placed at root


# References
- https://cloud.google.com/pubsub/docs/emulator
- https://cloud.google.com/pubsub/docs/create-topic-console
- https://cloud.google.com/pubsub/docs/publisher
- https://github.com/googleapis/python-pubsub/blob/main/samples/snippets/subscriber.py
