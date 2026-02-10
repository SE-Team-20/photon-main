


#!/bin/bash

echo "Installing Photon Laser Tag System..."

# Require root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root: sudo ./install.sh"
  exit 1
fi

# Update system packages
apt update

# Install required system packages
apt install -y python3 python3-pip python3-venv postgresql-client libpq-dev mpg123

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python libraries from requirements.txt
pip install --upgrade pip
pip install -r requirements.txt

echo "---------------------------------"
echo "Installation complete!"
echo "To run the program:"
echo "  source venv/bin/activate"
echo "  python3 main.py"
echo "---------------------------------"
