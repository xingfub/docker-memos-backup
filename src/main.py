from remotePathUtils import writeKey
from uploadutils.qiniuUtils import uploadFile as uploadFileQiniu,delFile as delFileQiniu
from uploadutils.alistUtils import uploadFile as uploadFileAlist,delFile as delFileAlist
from utils import getRemoteFileName as getRemoteFileName
from uploadutils.jianguoUtils import uploadFile as uploadFileJianguo,delFile as delFileJianguo
import os
from uploadutils.mailutils import uploadFile as uploadFileMail
from uploadutils.s3Utils import uploadFile as uploadFileS3,delFile as delFileS3
from backupUtils.mysqlBackup import downFileMySql



def uploadFile(localDbFile):
      # 2、上传文件
    print("2.uploadFile")
    remoteFileName=getRemoteFileName(localDbFile)
    # qiniuKey = uploadFileQiniu(localDbFile,remoteFileName)
    alistKey=uploadFileAlist(localDbFile,remoteFileName)
    jianguoKey=uploadFileJianguo(localDbFile,remoteFileName)
    s3Key=uploadFileS3(localDbFile,remoteFileName)
    uploadFileMail(localDbFile)
    # print(f"qiniuKey {qiniuKey} ")
    print(f"alistKey {alistKey} ")
    print(f" jianguoKey {jianguoKey}")
    print(f"s3Key {s3Key}")

    # 3、保存远程地址
    print("3.writeKey")
    d1,d2,d3=writeKey(s3Key,alistKey,jianguoKey)
    print(f"d1 {d1} d2 {d2} d3 {d3}")
    # 4、删除旧文件
    print("4.delFile")
    if d1:
        # delFileQiniu(d1)
        delFileS3(d1)
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
    
 