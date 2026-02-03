from remotePathUtils import writeKey
from qiniuUtils import uploadFile as uploadFileQiniu,delFile as delFileQiniu
from alistUtils import uploadFile as uploadFileAlist,delFile as delFileAlist
from utils import getRemoteFileName as getRemoteFileName
from jianguoUtils import uploadFile as uploadFileJianguo,delFile as delFileJianguo
import os
from mailutils import uploadFile as uploadFileMail
from backupUtils.mysqlBackup import downFileMySql



def uploadFile(localDbFile):
      # 2、上传文件
    print("2.uploadFile")
    remoteFileName=getRemoteFileName(localDbFile)
    qiniuKey = uploadFileQiniu(localDbFile,remoteFileName)
    alistKey=uploadFileAlist(localDbFile,remoteFileName)
    jianguoKey=uploadFileJianguo(localDbFile,remoteFileName)
    uploadFileMail(localDbFile)
    print(f"qiniuKey {qiniuKey} alistKey {alistKey} jianguoKey {jianguoKey}")
    # 3、保存远程地址
    print("3.writeKey")
    d1,d2,d3=writeKey(qiniuKey,alistKey,jianguoKey)
    print(f"d1 {d1} d2 {d2} d3 {d3}")
    # 4、删除旧文件
    print("4.delFile")
    if d1:
        delFileQiniu(d1)
    if d2:
        delFileAlist(d2)
    if d3:
        delFileJianguo(d3)

if __name__ == "__main__":
    # 1、下载文件
    
    localDbFile=downFileMySql()
    #文件长度大于0
    if  os.path.exists(localDbFile) and os.path.getsize(localDbFile) >100:
        # 2、上传文件
        uploadFile(localDbFile)
    else:
        print("zeabure downFile fail ,file size is 0")
    
 