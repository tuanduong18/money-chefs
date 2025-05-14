from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow your Expo app (running on a different port) to call this API

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({ 'msg': 'Hello from Flask!' })

@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    return jsonify({ 'youSent': data })

if __name__ == '__main__':
    # debug=True for auto-reload + nicer errors; change to False in prod
    app.run()
