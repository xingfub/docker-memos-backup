#!/bin/bash

IMAGE_NAME="memos"
CONTAINER_NAME="memos"

echo "Building Docker image..."
docker build -t "$IMAGE_NAME" .

if [ $? -ne 0 ]; then
    echo "Failed to build Docker image"
    exit 1
fi

echo "Stopping existing container if running..."
docker stop "$CONTAINER_NAME" 2>/dev/null || true
docker rm "$CONTAINER_NAME" 2>/dev/null || true

# 获取脚本的绝对路径
script_path=$(readlink -f "$0")
script_dir=$(dirname "$script_path")

echo "Starting container..."
docker run -d \
    --name "$CONTAINER_NAME" \
    --restart unless-stopped \
    -v $script_dir/.memos/:/var/opt/memos \
    -p 5230:80 \
    "$IMAGE_NAME"

echo "Container started successfully!"
echo "Container ID: $(docker ps -qf "name=$CONTAINER_NAME")"
