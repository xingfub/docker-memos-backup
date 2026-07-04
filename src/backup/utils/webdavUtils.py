# 添加当前目录到Python路径
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from webdav3.client import Client
from api.config import load_history as loadHistory, save_history as saveHistory
from datetime import datetime
class WebDAVClient:
    def __init__(self,webdavConfig):
        """
        初始化WebDAV客户端
        
        Args:
            webdav_url (str): WebDAV服务器URL
            username (str): 用户名
            password (str): 密码
        """
        self.options = {
            'webdav_hostname': webdavConfig['url'],
            'webdav_login': webdavConfig['username'],
            'webdav_timeout':300,
            'webdav_password': webdavConfig['password']
        }
        self.client = Client(self.options)
        self.client.verify = False  # 忽略SSL验证（可选）
        
    def upload_file(self, local_path, remote_path):
        try:
            if not os.path.exists(local_path):
                print(f"本地文件不存在: {local_path}")
                return False
             # 确保远程目录存在
            remote_dir = os.path.dirname(remote_path)
            if remote_dir and not self.client.check(remote_dir):
                self.client.mkdir(remote_dir)    
            print(f"确保远程目录存在: {remote_dir}")    
            # 上传文件
            self.client.upload_sync(remote_path=remote_path, local_path=local_path)
            print(f"文件上传成功: {local_path} -> {remote_path}")
            return True
        except Exception as e:
            print(f"文件上传失败: {str(e)}")
            return False
    
    def delete_file(self, remote_path):
        """
        从WebDAV服务器删除文件
        
        Args:
            remote_path (str): WebDAV服务器上的文件路径
            
        Returns:
            bool: 删除成功返回True，失败返回False
        """
        try:
            if not self.client.check(remote_path):
                print(f"远程文件不存在: {remote_path}")
                return False
                
            self.client.clean(remote_path)
            print(f"文件删除成功: {remote_path}")
            return True
        except Exception as e:
            print(f"文件删除失败: {str(e)}")
            return False



def uploadFile(local_file,remote_file,webdavConfig):
    print(f"------aList-----")
    client = WebDAVClient(webdavConfig)
    save_path = webdavConfig.get('save_path', '')
    if save_path:
        remote_file_ = f"{save_path}/{remote_file}" if not save_path.endswith('/') else f"{save_path}{remote_file}"
    else:
        remote_file_ = remote_file
    t=client.upload_file(local_file, remote_file_)
    if t:
        return remote_file_
    else:
        return None
        

def delFile(remote_file,webdavConfig):
    client = WebDAVClient(webdavConfig)
    client.delete_file(remote_file)


def main(localDbFile,remoteFileName,webdavConfig):
    """
    上传文件到WebDAV服务器,服务器的文件超过7天删除,返回是否执行成功
    Args:
        localDbFile (str): 本地文件路径
        remoteFileName (str): 远程文件名
    Returns:
        bool: 上传成功返回True，失败返回False
    """
    try:
        remote_file = uploadFile(localDbFile, remoteFileName,webdavConfig)
        if not remote_file:
            return False,"webdav上传失败"
        historyKey="webdav"
        history = loadHistory(historyKey)
        history.insert(0, remote_file)
        new_files = history[:7]
        saveHistory(historyKey,new_files)
        old_files = history[7:]
        # 删除超出7条的旧文件
        for old_file in old_files:
            if old_file:
                delFile(old_file,webdavConfig)
        return True,"webdav上传成功"
    except Exception as e:
        print(f'上传数据库出错: {e}')
        return False,f'上传数据库出错: {e}'
