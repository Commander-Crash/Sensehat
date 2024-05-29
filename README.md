# Led Matrix Display Messaging System
Led Matrix Display Messaging System for Sense HAT and Raspberry Pi
Overview

This Python script enables seamless messaging and display capabilities on the Sense HAT LED matrix for Raspberry Pi. It offers a flexible system for receiving messages over local Unix sockets or TCP sockets, parsing them, and displaying them on the LED matrix. Additionally, it supports optional audio alerts and text-to-speech functionality for enhanced user interaction.
Features

    Message Display: Messages sent to the script are displayed on the Sense HAT LED matrix with customizable attributes such as text color, scroll speed, and priority.
    Audio Alerts: Optional audio alerts can be played along with message display, allowing for multi-sensory notifications.
    Text-to-Speech: Utilizes the espeak tool for text-to-speech conversion, enhancing accessibility and user experience.
    Socket Communication: Supports communication over both local Unix sockets and TCP sockets, providing flexibility in message delivery.
    Threading: Utilizes threading for concurrent message handling, ensuring smooth operation even under heavy loads.

# Usage

    Installation:
        Ensure the Sense HAT library is installed on your Raspberry Pi.
        Clone the repository to your Raspberry Pi.

    Configuration:
        Adjust the script's settings as needed, such as the socket paths and default rotation of the LED matrix.

    Sending Messages:
        Send messages to the script using the specified message format: priority|text|color|speed|wav_path|use_espeak.
        Examples:
            echo "0|hello |[255,0,0]|0.1|path/to/audio/file.mp3|1" | nc <ip addr> <port>
            echo "1|urgent message|[0,255,0]|0.2||1" | nc -U /tmp/sense_hat_socket

    Customization:
        Customize message attributes such as priority, color, scroll speed, and audio alerts based on your requirements.
        Modify the script to integrate additional functionalities or customize the message handling process.

