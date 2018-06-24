from flask import Flask, request, jsonify
from api import API
from loader import Loader

app = Flask(__name__)

@app.route('/unique-users')
def unique_users():
  os = request.args.get('os')
  device = request.args.get('device')
  return jsonify(API().unique(os, device))

@app.route('/loyal-users')
def loyal_users():
  os = request.args.get('os')
  device = request.args.get('device')
  return jsonify(API().loyal(os, device))

if __name__ == '__main__':
  Loader()
  app.run(debug=True,host='0.0.0.0')
