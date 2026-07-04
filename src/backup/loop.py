import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .utils.webdavUtils import main as uploadFileWebdav
from .utils.mailutils import main as uploadFileMail
from .utils.s3Utils import main as uploadFileS3
from .utils.config import getRemoteFileName as getRemoteFileName
from .index import backup_memos_db as backupMemosDb
from api.config import load_config as loadConfig


def uploadFile(localDbFile):
      # 2、上传文件
    print("2.uploadFile")
    config=loadConfig()
    if not config:
        return (False, '备份配置文件不存在')
    remoteFileName=getRemoteFileName(localDbFile)
    result=[]
    if "s3"  in config and "endpoint_url"  in config['s3'] and config['s3']['endpoint_url']:
        s3Key=uploadFileS3(localDbFile,remoteFileName,config['s3'])
        result.append(s3Key,"s3备份成功" if s3Key else "s3备份失败")
    else:
        result.append (False, 'S3配置文件不存在s3配置')

    if "webdav"  in config and "url"  in config['webdav'] and config['webdav']['url']:
        webdavKey=uploadFileWebdav(localDbFile,remoteFileName,config['webdav'])
        result.append(webdavKey,"webdav备份成功" if webdavKey else "webdav备份失败")
    else:
        result.append (False, 'webdav配置文件不存在webdav配置')

    if "email"  in config and "to_email"  in config['email'] and config['email']['to_email']:
        emailKey=uploadFileMail(localDbFile,remoteFileName,config['email'])
        result.append(emailKey,"email备份成功" if emailKey else "email备份失败")
    else:
        result.append (False, 'Email配置文件不存在email配置')
    return result

def main():
    backupDbFile=backupMemosDb()
    if not backupDbFile[0]:
        return (False, backupDbFile[1])
    db_file_=   backupDbFile[1]
    result=uploadFile(db_file_)
    print(result)
    success=True
    msg=""
    for item in result:
        msg+=f"{item[1]},"
        if not item[0]:
            success=False
    return (success, msg)
