#!/bin/bash
# Photon-Main Automated Installer for Debian VM

set -e  # Stop on error

echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "Installing Python and venv..."
sudo apt install -y python3 python3-venv python3-pip

echo "Creating fresh virtual environment..."
rm -rf venv  # Ensure clean slate
python3 -m venv venv --system-site-packages

echo "Activating virtual environment and upgrading build tools..."
source venv/bin/activate
pip install --upgrade setuptools wheel

echo "Installing system dependencies (PostgreSQL client, build tools)..."
sudo apt install -y build-essential libpq-dev postgresql-client

echo "Installing Python packages from requirements..."
pip install PyQt6 psycopg2-binary
if [ -f config/requirements.txt ]; then
    pip install -r config/requirements.txt
else
    echo "Warning: config/requirements.txt not found, skipping."
fi

echo "Installation complete!"
echo "To run the software:"
echo "  source venv/bin/activate"
echo "  ./run.sh"

echo "Optional: to run the traffic generator for testing:"
echo "  python3 udp_test.py"
