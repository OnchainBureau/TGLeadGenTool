#!/bin/bash

# Create .Xauthority file
touch ~/.Xauthority

# Start the X virtual framebuffer
Xvfb :99 -screen 0 1024x768x16 -ac &

# Wait for Xvfb to be ready
sleep 2

# Set up X authority
xauth generate :99 . trusted
xauth add ${HOST}:99 . $(xxd -l 16 -p /dev/urandom)

# Start VNC server (useful for debugging)
x11vnc -display :99 -forever -nopw &

# Export display for GUI applications
export DISPLAY=:99

# Start the main Python application
python main.py