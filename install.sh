#updated install.sh: #!/bin/bash
# Photon-Main Automated Installer for Debian VM

set -e  # Stop on error if found

echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "Ensuring proper order of events..."
sudo apt install -y python3
sudo apt install -y python3-venv
python3 -m venv venv --system-site-packages
source venv/bin/activate
echo "Installing PIP..."
sudo apt install python3-pip
pip install --upgrade setuptools wheel

echo "Installing system dependencies..."
sudo apt install -y build-essential libpq-dev postgresql-client

echo "Installing Python dependencies..."
pip install PyQt6 psycopg2-binary
pip install -r config/requirements.txt


echo "Installation complete!"
echo "To run the software:"
echo "  source venv/bin/activate"
echo "  ./run.sh"

echo "Optional: to run the traffic generator for testing:"
echo "  python3 udp_test.py"
