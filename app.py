from flask import Flask, render_template,request
from flask_socketio import SocketIO, emit
import random
import string

app = Flask(__name__)
socketio = SocketIO(app)
active_connections = {} 


def generate_key():
    key_length = 4
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(key_length))

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    print('User connected')
    key = generate_key()
    active_connections[key] = request.sid
    emit('key_assigned', {'key': key})

@socketio.on('disconnect')
def on_disconnect():
    print('User disconnected')
    for key, sid in active_connections.items():
        if sid == request.sid:
            del active_connections[key]
            break

@socketio.on('send_message')
def send_message(data):
    key = data['key']
    message = data['message']
    if key in active_connections:
        recipient_sid = active_connections[key]
        emit('receive_message', {'message': message}, room=recipient_sid)
    else:
        emit('receive_message', {'message': 'Does not Match'}, room=request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True)
