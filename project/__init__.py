from flask import Flask, jsonify

app = Flask(__name__)

# set configuration
app.config.from_object('project.config.DevelopmentConfig')

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
