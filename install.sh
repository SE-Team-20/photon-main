#!/bin/bash
# Photon-Main Automated Installer for Debian VM

set -e  # Stop on error if found

echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv build-essential libpq-dev postgresql-client

echo "Creating Python virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing Python dependencies..."
if [ -f config/requirements.txt ]; then
    pip install -r config/requirements.txt
else
    pip install PyQt6 psycopg2-binary pygame
fi

echo "Installation complete!"
echo "To run the software:"
echo "  source venv/bin/activate"
echo "  ./run.sh"

echo "Optional: to run the traffic generator for testing:"
echo "  python3 udp_test.py"
