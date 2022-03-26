from tensorflow import keras
from tensorflow.keras.datasets import fashion_mnist as mnist
from tensorflow.keras.utils import to_categorical

from kafka import KafkaConsumer, KafkaProducer
import os
import json
import uuid
from concurrent.futures import ThreadPoolExecutor

def load_data():
    (X_train, y_train), (X_test, y_test) = keras.datasets.fashion_mnist.load_data()
    X_train = X_train.reshape((X_train.shape[0], 28, 28, 1))
    X_test = X_test.reshape((X_test.shape[0], 28, 28, 1))
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

    return (X_train, y_train), (X_test, y_test)

def prep_pixels(dataset):
    train_norm = dataset.astype('float32')
    dataset = dataset / 255.0
    return dataset

def model_pred(start_idx=0, end_idx=1):
    y_pred = model.predict(X_test_prep[start_idx:end_idx])
    y_classes = y_pred.argmax(axis=-1)
    label_resp = [labels[y_classes[i]] for i in range(len(y_classes))]
    return ",".join(label_resp)

def model_inference(data):
    start_idx = data['start_idx']
    end_idx = data['end_idx']

    predicted_classes = model_pred(start_idx, end_idx)
    print('Model Inference...')
    print(predicted_classes)


# Kafka Consumer
TOPIC_NAME = "INFERENCE"
KAFKA_SERVER = "localhost:9092"

consumer = KafkaConsumer(
    TOPIC_NAME,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
)

# loading train and test data from keras
(X_train, y_train), (X_test, y_test) = load_data()

# preprocessing the data for test set
X_test_prep = prep_pixels(X_test)

# label mapping
labels = {
    0 : "T-shirt/top", 1: "Trouser", 2: "Pullover",
    3: "Dress", 4: "Coat", 5: "Sandal", 6: "Shirt",
    7: "Sneaker", 8: "Bag", 9: "Ankle Boot"
}

# loading trained model
model = keras.models.load_model('model.h5')

for message in consumer:
    index_range_x_test = message.value
    model_inference(index_range_x_test)
