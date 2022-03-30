import os
import traceback
from datetime import datetime

from google.cloud import pubsub_v1
from tensorflow import keras
from tensorflow.keras.datasets import fashion_mnist as mnist
from tensorflow.keras.utils import to_categorical


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

def model_inference(message: pubsub_v1.subscriber.message.Message) -> None:
    # print(f"Received {message}.")
    message.ack()

    data = message.data.decode('utf-8')
    print(data)

    attrs = message.attributes

    # print(attrs)

    start_idx = int(attrs['start_idx'])
    end_idx = int(attrs['end_idx'])

    predicted_classes = model_pred(start_idx, end_idx)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f'[{now}] Model Inference [{start_idx} - {end_idx}]')
    print(predicted_classes)


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vcai-creds.json'

project_id = "inspiring-bonus-140103"
subscription_id = "vectorai-subscription"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

streaming_pull_future = subscriber.subscribe(subscription_path, callback=model_inference)
print(f"Listening for messages on {subscription_path}..\n")

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

with subscriber:
    try:
        print('starting stream...')
        streaming_pull_future.result()
    except:
        print(traceback.format_exc())
        print('ending stream...')
        streaming_pull_future.cancel()
        streaming_pull_future.result()
