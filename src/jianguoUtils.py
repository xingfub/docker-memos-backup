import requests
import os
from urllib.parse import urljoin



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
            'webdav_hostname': 'https://dav.jianguoyun.com/dav',
            'webdav_login': "proud2008@qq.com",
            'webdav_password': "aeddig2zsy33wqnn"
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
    
    def get_file_list(self, remote_path):
        """
        获取WebDAV服务器上的文件列表
        
        Args:
            remote_path (str): WebDAV服务器上的目录路径
            
        Returns:
            list: 文件列表，每个元素包含文件名和路径
        """
        try:
            if not self.client.check(remote_path):
                print(f"远程目录不存在: {remote_path}")
                return []
                
            # 获取文件列表
            file_list = self.client.list(remote_path)
            print(f"获取文件列表成功: {remote_path}")
            print(f"文件数量: {len(file_list)}")
            for file in file_list:
                print(f"  - {file}")
            return file_list
        except Exception as e:
            print(f"获取文件列表失败: {str(e)}")
            return []



def uploadFile(local_file,remote_file):
    client = WebDAVClient()
    remote_file_ = f"/imemos/sqlBackup/{remote_file}"
    client.upload_file(local_file, remote_file_)
    return remote_file_
        

def delFile(remote_file):
    client = WebDAVClient()
    client.delete_file(remote_file)


if __name__ == "__main__":
    # 测试上传文件
    # local_file = "main.py"
    # remote_file = "test.txt"
    # uploadFile(local_file,remote_file)
    
    # 测试获取文件列表
    client = WebDAVClient()
    remote_dir = "/imemos/sqlBackup"
    client.get_file_list(remote_dir)















