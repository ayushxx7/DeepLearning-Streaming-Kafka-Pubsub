import json
import os

from flask import Flask, jsonify, redirect, render_template, request, url_for
from google.cloud import pubsub_v1
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message_broker = request.form['message_broker']
        start_idx = request.form['start_idx']
        end_idx = request.form['end_idx']

        print(message_broker, start_idx, end_idx)

        if message_broker == 'kafka':
            return redirect(url_for('kafkaProducer', start_idx=start_idx, end_idx=end_idx))
        elif message_broker == 'pubsub':
            return redirect(url_for('googlePublisher', start_idx=start_idx, end_idx=end_idx))

    else:
        return render_template('form.html')



if __name__ == '__main__':
    app.run(debug=True)
