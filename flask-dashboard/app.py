from flask import Flask, jsonify, render_template, request
import random
import datetime
import logging
import redis
from flask_cors import CORS


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app)

redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/randomdata')
def get_data():
    data = {
        "time": datetime.datetime.now(),
        "value": random.randint(1, 100),
    }
    return jsonify(data)

@app.route('/api/data', methods=['GET'])
def fetch_data():
    prefix = request.args.get('prefix')

    matching_keys = redis_client.keys(f"{prefix}*")
    data = []

    for key in matching_keys:
        key_type = redis_client.type(key)
        if key_type == 'hash':
            data.append(redis_client.hgetall(key))

    return jsonify({"prefix": prefix, "results": data})

if __name__  == "__main__":
     app.run(host="0.0.0.0", port=5000, debug=True)
