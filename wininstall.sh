#!/bin/bash
# Photon-Main Automated Installer for Debian 11

set -e

cd "$(dirname "$0")"

echo "Adding contrib, non-free, and backports repos..."
sudo sed -i 's/ main$/ main contrib non-free/' /etc/apt/sources.list
if ! grep -q "bullseye-backports" /etc/apt/sources.list; then
    echo "deb http://deb.debian.org/debian bullseye-backports main contrib non-free" | sudo tee -a /etc/apt/sources.list
fi

echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "Installing Python 3.11 from backports..."
sudo apt install -y -t bullseye-backports python3.11 python3.11-venv python3.11-dev

echo "Installing Qt platform dependencies..."
sudo apt install -y \
    libxcb-util1 \
    libxcb-xinerama0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-render-util0 \
    libxkbcommon-x11-0 \
    libgl1
sudo apt install -y libxcb-cursor0 || echo "libxcb-cursor0 not available, skipping."

echo "Installing audio and GStreamer dependencies..."
sudo apt install -y \
    libpulse0 \
    pulseaudio \
    libgstreamer1.0-0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav

echo "Installing database and build dependencies..."
sudo apt install -y build-essential libpq-dev postgresql-client

echo "Creating fresh virtual environment with Python 3.11..."
rm -rf venv
python3.11 -m venv venv

echo "Activating virtual environment and installing Python packages..."
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install PyQt6 psycopg2-binary pygame

echo "--------------------------------------------------"
echo "Installation complete!"
echo ""
echo "To run the software:"
echo "  ./run.sh"
echo "--------------------------------------------------"
