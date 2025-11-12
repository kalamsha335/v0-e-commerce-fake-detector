#!/bin/bash

# Realtime producer script
# Run synthetic product listings through the detection pipeline

set -e

# Configuration
DURATION=${1:-60}  # seconds
INTERVAL=${2:-3}   # seconds between listings
FAKE_RATE=${3:-0.3}  # 30% fake by default

echo "Starting Fake Product Detector Producer Demo"
echo "=============================================="
echo "Duration: $DURATION seconds"
echo "Interval: $INTERVAL seconds"
echo "Fake Rate: $(echo "scale=1; $FAKE_RATE * 100" | bc)%"
echo ""

# Check if API is running
if ! curl -s http://localhost:3000/api/analyze > /dev/null 2>&1; then
    echo "ERROR: Backend API not running at http://localhost:3000"
    echo "Please start with: docker-compose up"
    exit 1
fi

# Run producer
cd ml
python producer.py \
    --duration $DURATION \
    --interval $INTERVAL \
    --fake-rate $FAKE_RATE \
    --api-url http://localhost:3000/api/analyze
