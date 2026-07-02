#!/bin/bash

echo "Starting memos service..."
/var/opt/memos/memos &

echo "Starting Flask admin service..."
cd /app/src && python main.py &

echo "Starting nginx..."
nginx -g "daemon off;"
