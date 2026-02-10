#!/bin/bash

echo "Installing Photon Laser Tag System..."

# Require root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root: sudo ./install.sh"
  exit 1
fi

# Update system
apt update

# Install system packages
apt install -y python3 python3-pip python3-venv postgresql-client libpq-dev mpg123

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python libraries
pip install PyQt6 psycopg2-binary

echo "---------------------------------"
echo "Installation complete!"
echo "To run the program:"
echo "  source venv/bin/activate"
echo "  python3 main.py"
echo "---------------------------------"


# How to run this script
# First need to change its mode via this command (chmod +x install.sh)
# to run (sudo ./install.sh)

