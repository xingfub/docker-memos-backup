基于 memos 项目，
添加python环境 页面管理功能实现 备份还原功能

添加nginx 反向代理
admin 指向 python的管理页面 实现备份还原


# 查看memos进程占用5230端口
ss -tulnp | grep memos
# 手动重启memos
/usr/local/memos/memos
/usr/local/memos/memos &
# 停止memos
pkill memos