#构建多架构镜像，并上传到阿里云，docker hub
#!/bin/bash

sudo apt update
# 安装docker buildx插件，用于构建多架构镜像
sudo apt install docker-buildx-plugin
# 若安装失败，手动下载插件，安装
# mkdir -p ~/.docker/cli-plugins
# curl -sL "https://github.com/docker/buildx/releases/download/v0.17.0/buildx-v0.17.0.linux-amd64" -o ~/.docker/cli-plugins/docker-buildx
# chmod +x ~/.docker/cli-plugins/docker-buildx
# cd ~/.docker/cli-plugins
# ./docker-buildx
#验证buildx是否安装成功,查看版本
docker buildx version

sudo apt update
# 安装dbus，用于构建多架构镜像
sudo apt install dbus dbus-x11
sudo systemctl restart dbus

# 创建一个支持多架构的构建实例
sudo docker buildx create --name multiarch --use
sudo docker buildx inspect --bootstrap

IMAGE_NAME="registry.cn-hangzhou.aliyuncs.com/xingfub/memos:0.25.1"
sudo docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t "$IMAGE_NAME" \
  --push .

