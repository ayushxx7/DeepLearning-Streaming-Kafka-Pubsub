from flask import Flask, request, jsonify
from google.cloud import pubsub_v1
import os
import json
from kafka import KafkaProducer

# KAFKA SETUP
TOPIC_NAME = 'INFERENCE'
KAFKA_SERVER = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

# PUBSUB SETUP
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vcai-creds.json'
publisher = pubsub_v1.PublisherClient()

pub_sub_topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id='inspiring-bonus-140103',
    topic='MODEL-INFERENCE'
)

app = Flask(__name__)

@app.route('/kafka/push-to-consumer', methods=['GET', 'POST'])
def kafkaProducer():
    req = request.args
    start_idx = int(request.args.get('start_idx'))
    end_idx = int(request.args.get('end_idx'))

    data = {
        'start_idx': start_idx,
        'end_idx': end_idx,
    }

    producer.send(TOPIC_NAME, data)
    producer.flush()

    print("Sent to consumer - local kafka")

    return jsonify({
        "message_queue": "kafka",
        "start_idx": start_idx,
        "end_idx": end_idx
    })

@app.route('/pubsub/push-to-consumer', methods=['GET', 'POST'])
def googlePublisher():
    req = request.args
    start_idx = request.args.get('start_idx')
    end_idx = request.args.get('end_idx')

    future = publisher.publish(pub_sub_topic_name,
                               b'pubsub - model inference',
                               start_idx=start_idx,
                               end_idx=end_idx)

    print(future.result())

    print("Sent to consumer - cloud pub sub")

    return jsonify({
        "message_queue": "pubsub",
        "start_idx": start_idx,
        "end_idx": end_idx
    })

if __name__ == '__main__':
    app.run(debug=True)
