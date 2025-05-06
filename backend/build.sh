#!/bin/bash

echo "🔧 Installing dependencies..."
pip install -r requirements.txt

echo "🚀 Starting BlueJay backend..."
python main.py
