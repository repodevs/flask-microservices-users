import os
from flask import Flask, jsonify

app = Flask(__name__)

# set configuration
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
