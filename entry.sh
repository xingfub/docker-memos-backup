#!/bin/sh

# 2. 后台启动三个服务
nginx &
python /app/src/main.py &
/usr/local/memos/memos &

# 前台永久阻塞，防止容器退出
sleep infinity