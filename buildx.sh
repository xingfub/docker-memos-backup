#构建多架构镜像，并上传到阿里云，docker hub
#!/bin/bash
# 创建一个支持多架构的构建实例
docker buildx create --name multiarch --use
docker buildx inspect --bootstrap


IMAGE_NAME="xingfub/memos:0.25.1"
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t "$IMAGE_NAME" \
  --push .

