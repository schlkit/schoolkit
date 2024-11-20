from flask import Flask, send_from_directory, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
from collections import deque
import json

app = Flask(__name__, static_folder='site')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Database configuration
DB_PATH = 'chat.db'

# Create database and table
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Helper function to dict format
def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

# Create a deque to store recent messages (limited to last 100 messages)
recent_messages = deque(maxlen=100)

# Chat WebSocket events
@socketio.on('connect')
def handle_connect():
    # Send last 50 messages to newly connected client
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages ORDER BY timestamp DESC LIMIT 50")
    messages = cursor.fetchall()
    emit('message_history', messages)
    conn.close()

@socketio.on('new_message')
def handle_message(data):
    username = data['username']
    message = data['message']
    
    # Store message in database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (username, message, timestamp) VALUES (?, ?, ?)",
        (username, message, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    )
    conn.commit()
    conn.close()
    
    # Broadcast message to all clients
    emit('new_message', {
        'username': username,
        'message': message,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }, broadcast=True)

@socketio.on('message')
def handle_message(data):
    username = data.get('username', 'Anonymous')
    message = data.get('message', '')
    timestamp = datetime.now().strftime('%H:%M')
    
    message_data = {
        'username': username,
        'message': message,
        'timestamp': timestamp
    }
    
    # Store the message
    recent_messages.append(message_data)
    
    # Broadcast to all clients
    emit('message', message_data, broadcast=True)
    
    # Also update the preview for homepage
    emit('recent messages', list(recent_messages)[-2:], broadcast=True)

@socketio.on('get_recent_messages')
def handle_get_recent():
    # Send last 2 messages to the requesting client
    emit('recent messages', list(recent_messages)[-2:])

# Existing routes
@app.route('/')
def serve_index():
    return send_from_directory('site', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('site', filename)

if __name__ == "__main__":
    socketio.run(app, debug=True)
