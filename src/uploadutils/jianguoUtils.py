import requests
import os
from urllib.parse import urljoin
import urllib3

# 禁用InsecureRequestWarning警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
            'webdav_hostname': 'https://dav.jianguoyun.com',
            'webdav_login': "proud2008@qq.com",
            'webdav_password': "aeddig2zsy33wqnn",
            'webdav_timeout':300,
            'webdav_verify':False,
            'webdav_root':"/dav/imemos/sqlBackup/"
        }
        self.client = Client(self.options)
        self.client.verify = False  # 忽略SSL验证（可选）
        
    def upload_file(self, local_path, remote_path):
        try:
            if not os.path.exists(local_path):
                print(f"本地文件不存在: {local_path}")
                return False
            remote_parent=self.options['webdav_root']
            t=self.client.check(remote_path=remote_parent)
            print(f"检查目录是否存在: {remote_parent} {t}")
            # 上传文件
            remote_path=remote_parent+os.path.basename(local_path)
            self.client.upload_sync(remote_path='/dav/1.txt', local_path=local_path)
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
    
    def get_file_list(self):
        """
        获取WebDAV服务器上的文件列表
        
        Args:
            remote_path (str): WebDAV服务器上的目录路径
            
        Returns:
            list: 文件列表，每个元素包含文件名和路径
        """
      
        # 获取文件列表
        file_list = self.client.list()
        print(f"获取文件列表成功 1: {file_list}")
        # print(f"获取文件列表成功 2: {self.client.list(remote_path="/",get_info=True)}")
        # try:
        #     print(f"获取文件列表成功 3: {self.client.list(remote_path="/dav/certificate/",get_info=True)}")
        # except Exception as e:
        #         print(f"获取文件列表失败: {str(e)}")
        # for file in file_list:
        #     print(f"文件: {file}")
        #     try:
        #         print(self.client.list(remote_path=file))
        #     except Exception as e:
        #         print(f"获取文件列表失败: {str(e)}")



def uploadFile(local_file,remote_file):
    print(f"------jianguo-----")
    client = WebDAVClient()
    remote_file_ = f"{remote_file}"
    t=client.upload_file(local_file, remote_file_)
    if t:
        return remote_file_
    else:
        return None
        

def delFile(remote_file):
    client = WebDAVClient()
    client.delete_file(remote_file)


if __name__ == "__main__":
    # 测试上传文件
    local_file = "main.py"
    remote_file = "test.txt"
    uploadFile(local_file,remote_file)
    
    # 测试获取文件列表
    # client = WebDAVClient()
    # client.get_file_list()















