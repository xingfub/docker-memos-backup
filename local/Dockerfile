FROM memos-admin 

COPY ../src/ /app/src
COPY ../nginx/yps.conf /etc/nginx/http.d/default.conf
COPY ../entry.sh /entry.sh
RUN chmod +x /entry.sh
# 赋予执行权限
# RUN chmod +x /usr/local/memos/memos /entry.sh

# 核心：ENTRYPOINT 执行脚本，CMD置空
ENTRYPOINT ["/entry.sh"]
CMD []
