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

SEEN_SET_NAME = "seen_keys"

@app.route('/api/historical', methods=['GET'])
def fetch_historical():
    """
    Fetch all historical data on page refresh without filtering for 'seen' state.
    """
    prefix = request.args.get('prefix')

    matching_keys = redis_client.keys(f"{prefix}*")
    twitter_data = []
    reddit_data = []

    for key in matching_keys:
        key_type = redis_client.type(key)
        if key_type == 'hash':
            d = redis_client.hgetall(key)
            if 'key' in d:
                if d['key'] == 'reddit_mean':
                    reddit_data.append(d)
                elif d['key'] == 'twitter_mean':
                    twitter_data.append(d)

    # Sort by timestamp
    reddit_data = sorted(reddit_data, key=lambda i: i['timestamp'])
    twitter_data = sorted(twitter_data, key=lambda i: i['timestamp'])

    return jsonify({"prefix": prefix, "reddit_mean": reddit_data, 'twitter_data': twitter_data})


@app.route('/api/latest', methods=['GET'])
def fetch_latest():
    """
    Fetch only the latest unseen data every 3 seconds.
    """
    prefix = request.args.get('prefix')

    matching_keys = redis_client.keys(f"{prefix}*")

    matching_keys = sorted(matching_keys, key=lambda i: i.split(':')[1].split('::')[0], reverse=True)

    twitter_data = []
    reddit_data = []

    unseen_keys = [key for key in matching_keys if not redis_client.sismember(SEEN_SET_NAME, key)]

    for key in unseen_keys:
        key_type = redis_client.type(key)
        if key_type == 'hash':
            d = redis_client.hgetall(key)
            if 'key' in d:
                if d['key'] == 'reddit_mean':
                    reddit_data.append(d)
                elif d['key'] == 'twitter_mean':
                    twitter_data.append(d)

    for key in unseen_keys:
        redis_client.sadd(SEEN_SET_NAME, key)

    return jsonify({"prefix": prefix, "reddit_mean": reddit_data, 'twitter_data': twitter_data})
if __name__  == "__main__":
     app.run(host="0.0.0.0", port=5000, debug=True)