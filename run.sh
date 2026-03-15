#!/bin/bash
# Move to the directory where the script is located
cd "$(dirname "$0")"

if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Environment activated. Launching Photon..."
    python3 main.py
else
    echo "Error: venv not found. Please run ./install.sh first."
    exit 1
fi