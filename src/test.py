import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from backup.loop import main2 as backupMain2
# backupMain2((True,"../local/memos_prod.db"))


from backup.utils.webdavUtils import WebDAVClient
config={
    "url":"https://alist.xingfub.dpdns.org/dav/",
    "username":"admin",
    "password":"ALISThu0303"}
client = WebDAVClient(config)
client.upload_file("../local/memos_prod.db","a/tools/a.db")

# config={
#     "url":"https://dav.jianguoyun.com/dav/imemos/",
#     "username":"proud2008@qq.com",
#     "password":"a5ewus8eq5wxq83e"}
# client = WebDAVClient(config)
# print(client.list_file("/"))
# client.upload_file("../local/memos_prod.db","a.db")
