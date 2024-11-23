from flask import Flask, jsonify, render_template
import random
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/data')
def get_data():
     data = {
        "time": datetime.datetime.now(),
        "value": random.randint(1, 100),
    }
     return jsonify(data)

if __name__  == "__main__":
     app.run(host="0.0.0.0", port=5000, debug=True)
