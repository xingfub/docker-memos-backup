#!/bin/bash

IMAGE_NAME="memos-admin2"
CONTAINER_NAME="memos-admin-container"

echo "Building Docker image..."
docker build -t "$IMAGE_NAME" .

if [ $? -ne 0 ]; then
    echo "Failed to build Docker image"
    exit 1
fi

echo "Stopping existing container if running..."
docker stop "$CONTAINER_NAME" 2>/dev/null || true
docker rm "$CONTAINER_NAME" 2>/dev/null || true

echo "Starting container..."
docker run -d \
    --name "$CONTAINER_NAME" \
    --restart unless-stopped \
    -p 8080:80 \
    "$IMAGE_NAME"

echo "Container started successfully!"
echo "Container ID: $(docker ps -qf "name=$CONTAINER_NAME")"
