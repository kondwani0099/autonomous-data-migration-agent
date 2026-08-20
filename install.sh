#!/usr/bin/env bash
# Uniplexity Migration Agent — Environment Installer Script
set -e

AFAC_REF="v1.0.0"

echo "=========================================="
echo "Installing Uniplexity Migration Agent ($AFAC_REF)"
echo "=========================================="

echo "[1/3] Setting up Python backend environment..."
if [ -d "backend" ]; then
    cd backend
    python3 -m venv venv || python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    cd ..
fi

echo "[2/3] Setting up Node.js frontend environment..."
if [ -d "frontend" ]; then
    cd frontend
    npm install
    cd ..
fi

echo "[3/3] Running workspace validation..."
python3 scripts/validate.py || python scripts/validate.py

echo "Installation complete!"
