from webdav3.client import Client
import os
from datetime import datetime
from utils import __getSqlFileName
class WebDAVClient:
    def __init__(self):
    
        self.options = {
            'webdav_hostname': 'https://dav.jianguoyun.com',
            'webdav_login': "proud2008@qq.com",
            'webdav_password': "JIANGUOYUNhu0303",
            'verify': False
        }
        self.client = Client(self.options)
        
    def upload_file(self, local_path, remote_path):
        """
        上传文件到WebDAV服务器
        
        Args:
            local_path (str): 本地文件路径
            remote_path (str): WebDAV服务器上的目标路径
            
        Returns:
            bool: 上传成功返回True，失败返回False
        """
        try:
            if not os.path.exists(local_path):
                print(f"本地文件不存在: {local_path}")
                return False
            print(f"本地文件存在: {local_path}")
            # 确保远程目录存在
            # remote_dir = os.path.dirname(remote_path)
            # if remote_dir and not self.client.check(remote_dir):
            #     self.client.mkdir(remote_dir)    
            # print(f"确保远程目录存在: {remote_dir}")
            # 上传文件
            self.client.upload_sync(remote_path="/dav", local_path=local_path)
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

# 使用示例
if __name__ == "__main__":
    # 配置WebDAV连接信息
   
    
    # 创建客户端实例
    client = WebDAVClient()
    
    # 上传文件示例
    local_file = "requirements.txt"
    remote_file = __getSqlFileName()
    print(f"远程文件路径: {remote_file}")
    # client.upload_file(local_file, "/")
    # 删除文件示例
    client.delete_file("c/dl-file/sqlBackup/a.txt")




def uploadFile(local_file,remote_file):
        return None
        

def delFile(remote_file):
   return None