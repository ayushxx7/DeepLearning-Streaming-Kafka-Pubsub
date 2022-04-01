import json
import traceback
from datetime import datetime

from kafka import KafkaConsumer
from tensorflow import keras
from tensorflow.keras.datasets import fashion_mnist as mnist
from tensorflow.keras.utils import to_categorical


def load_data():
    """Load MNIST dataset

    Returns
    -------
        tuple: (train_images, train_labels), (test_images, test_labels)
    """
    (X_train, y_train), (X_test, y_test) = keras.datasets.fashion_mnist.load_data()
    X_train = X_train.reshape((X_train.shape[0], 28, 28, 1))
    X_test = X_test.reshape((X_test.shape[0], 28, 28, 1))
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

    return (X_train, y_train), (X_test, y_test)

def prep_pixels(dataset):
    """Normalize dataset to [0, 1] range

    Parameters
    ----------
        dataset: numpy.ndarray
            dataset to be prepared

    Returns
    -------
        numpy.ndarray
            prepared dataset
    """
    dataset = dataset.astype('float32')
    dataset = dataset / 255.0
    return dataset

def model_pred(start_idx=0, end_idx=1):
    """Prediction on test set from start_idx to end_idx

    Parameters
    ----------
        start_idx: int
            start index of the batch
        end_idx: int
            end index of the batch

    Returns
    -------
        str
            predicted classes
    """
    y_pred = model.predict(X_test_prep[start_idx:end_idx])
    y_classes = y_pred.argmax(axis=-1)
    label_resp = [labels[y_classes[i]] for i in range(len(y_classes))]
    return ",".join(label_resp)

def model_inference(data):
    """Print the model inference to console

    Parameters
    ----------
        data: dict
            data to be inferred

    Returns
    -------
    None
    """
    start_idx = data['start_idx']
    end_idx = data['end_idx']

    predicted_classes = model_pred(start_idx, end_idx)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f'[{now}] Model Inference [{start_idx} - {end_idx}]')
    print(predicted_classes)


# Kafka Consumer
TOPIC_NAME = "INFERENCE"
KAFKA_SERVER = "localhost:9092"

consumer = KafkaConsumer(
    TOPIC_NAME,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    bootstrap_servers=KAFKA_SERVER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='consumer-group-1'
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
    try:
        index_range_x_test = message.value
        model_inference(index_range_x_test)
    except:
        print(traceback.format_exc())
