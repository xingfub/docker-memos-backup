#!/bin/bash

IMAGE_NAME="xingfub/memos:0.25.1"
CONTAINER_NAME="memos"

# 删除镜像，构建镜像
# sudo docker rmi "$IMAGE_NAME"
# sudo docker build -t "$IMAGE_NAME" .

# 获取脚本的绝对路径
script_path=$(readlink -f "$0")
# 获取脚本所在的目录
script_dir=$(dirname "$script_path")

echo "Stopping existing container if running..."
docker stop "$CONTAINER_NAME" 2>/dev/null || true
docker rm "$CONTAINER_NAME" 2>/dev/null || true

echo "Starting container..."
sudo docker run -d \
    --name "$CONTAINER_NAME" \
    --restart unless-stopped \
    -v $script_dir/.memos/:/var/opt/memos \
    -p 5230:80 \
    "$IMAGE_NAME"

echo "Container started successfully!"
echo "Container ID: $(docker ps -qf "name=$CONTAINER_NAME")"
