from webdav3.client import Client
import os
from datetime import datetime
class WebDAVClient:
    def __init__(self):
        """
        初始化WebDAV客户端
        
        Args:
            webdav_url (str): WebDAV服务器URL
            username (str): 用户名
            password (str): 密码
        """
        self.options = {
            'webdav_hostname': 'https://a.xingfub.dpdns.org/dav/',
            'webdav_login': "admin",
            'webdav_timeout':300,
            'webdav_password': "ALISThu0303"
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



def uploadFile(local_file,remote_file):
    print(f"------aList-----")
    client = WebDAVClient()
    remote_file_ = f"/a/imemos/sqlBackup/{remote_file}"
    t=client.upload_file(local_file, remote_file_)
    if t:
        return remote_file_
    else:
        return None
        

def delFile(remote_file):
    client = WebDAVClient()
    client.delete_file(remote_file)