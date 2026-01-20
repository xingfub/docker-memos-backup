# 编辑crontab配置
crontab -e

# 添加以下行（选择一种方式）

# 方式1：每天固定时间执行（如每天凌晨2点执行）
0 2 * * * python3 /home/ubuntu/light/memos/backsql.py > /home/ubuntu/light/memos/backsql.log 2>&1


# 查看当前crontab配置
crontab -l

# 删除所有crontab配置
crontab -r