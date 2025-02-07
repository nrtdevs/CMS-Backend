from flask_socketio import emit
from app.database import socketio

@socketio.on('connect')
def handle_connect():
    print("✅ Client connected")  # ✅ Check if this prints
    emit('server_response', {'message': 'Connected to server!'}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    print("❌ Client disconnected")  # ✅ Check if this prints

@socketio.on('message')
def handle_message(data):
    print(f"📩 Received message: {data}")  # ✅ Check if this prints
    emit('server_response', {'message': 'Message received!'}, broadcast=True)
