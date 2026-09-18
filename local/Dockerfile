FROM xingfub/memos:0.25.1

COPY ../src/ /app/src
COPY ../nginx/yps.conf /etc/nginx/http.d/default.conf
COPY ../entry.sh /entry.sh
RUN chmod +x /entry.sh
# 赋予执行权限
# RUN chmod +x /usr/local/memos/memos /entry.sh

# 核心：ENTRYPOINT 执行脚本，CMD置空
# ENTRYPOINT ["/entry.sh"]
# CMD []

# 树霉派设备使用下面这个，使用sh文件会报文件格式错误无法启动
ENTRYPOINT []
CMD ["sh", "-c", "nginx & python /app/src/main.py & /usr/local/memos/memos & exec sleep infinity"]

