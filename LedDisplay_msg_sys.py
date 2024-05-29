#!/usr/bin/env python3

# Led Matrix display messageing system for the sensehat and raspberry pi
# By Commander Crash
# v0.9
# echo priority|text|color|speed|wav_path|use_espeak
# How to use: echo "0|hello |[255,0,0]|0.1|path/to/wav/or/mp3/file.mp3|1" | nc <ip addr> <port> # for over the lan/net
# How to use: echo "0|hello |[255,0,0]|0.1|path/to/wav/or/mp3/file.mp3|1" | nc -U /tmp/sense_hat_socket # Local socket
# or echo "0|hello |[255,0,0]|0.1||" | nc -U /tmp/sense_hat_socket # no audio or espeak

import os
import socket
import select
from sense_hat import SenseHat
import subprocess
import queue
import threading

sense = SenseHat()
sense.set_rotation(90)

sock_path = "/tmp/sense_hat_socket"
tcp_port = 5150  # Use the new port

# Remove existing socket if present
try:
    os.unlink(sock_path)
except OSError:
    if os.path.exists(sock_path):
        raise

# Create and bind the local Unix socket
local_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
local_sock.bind(sock_path)
local_sock.listen(1)

# Create and bind the network TCP socket
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.bind(('0.0.0.0', tcp_port))
tcp_sock.listen(5)

# Define the message structure
class Message:
    def __init__(self, text, priority, color, speed, wav_path, use_espeak):
        self.text = text
        self.priority = priority
        self.color = color
        self.speed = speed
        self.wav_path = wav_path
        self.use_espeak = use_espeak

    def __lt__(self, other):
        return self.priority < other.priority

# Function to play alert sound
def play_alert_sound(wav_path):
    if wav_path:
        subprocess.Popen(['mpg123', wav_path])

# Message handler thread function
def message_handler():
    while True:
        priority, msg = message_queue.get()
        print(f"Handling message: {msg.text}")  # Debug statement
        if msg.wav_path:
            play_alert_sound(msg.wav_path)
        if msg.use_espeak:
            subprocess.run(["espeak", msg.text], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sense.show_message(msg.text, text_colour=msg.color, scroll_speed=msg.speed)
        message_queue.task_done()

# Function to add message to the priority queue
def add_message_to_queue(msg):
    print(f"Queueing message: {msg.text} with priority {msg.priority}")  # Debug statement
    message_queue.put((msg.priority, msg))

# Global variables
message_queue = queue.PriorityQueue()

# Start the message handler thread
handler_thread = threading.Thread(target=message_handler)
handler_thread.daemon = True
handler_thread.start()

def parse_and_queue_message(data):
    try:
        print(f"Received data: {data}")  # Debug statement
        priority, text, color_str, speed, wav_path, use_espeak = data.split("|")
        color = list(map(int, color_str.strip('[]').split(",")))
        speed = float(speed)
        use_espeak = bool(int(use_espeak.strip())) if use_espeak.strip() else False
        msg = Message(text, int(priority), color, speed, wav_path, use_espeak)
        add_message_to_queue(msg)
    except Exception as e:
        print(f"Failed to parse message: {e}")  # Debug statement

# Main loop to handle both sockets
while True:
    read_sockets, _, _ = select.select([local_sock, tcp_sock], [], [])
    for sock in read_sockets:
        if sock is local_sock:
            connection, _ = local_sock.accept()
            data = connection.recv(1024).decode().strip()
            if data:
                parse_and_queue_message(data)
            connection.close()
        elif sock is tcp_sock:
            connection, _ = tcp_sock.accept()
            data = connection.recv(1024).decode().strip()
            if data:
                parse_and_queue_message(data)
            connection.close()
