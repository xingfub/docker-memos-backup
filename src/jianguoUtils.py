from webdav3.client import Client
import os
from datetime import datetime
from utils import __getSqlFileName
class WebDAVClient:
    def __init__(self):
    
        self.options = {
            'webdav_hostname': 'https://dav.jianguoyun.com/dav',
            'webdav_login': "proud2008@qq.com",
            'webdav_password': "JIANGUOYUNhu0303",
            'verify': False
        }
        self.client = Client(self.options)
        
    def upload_file(self, local_path, remote_path):
        try:
            if not os.path.exists(local_path):
                print(f"本地文件不存在: {local_path}")
                return False
            print(f"本地文件存在: {local_path}")
            # 确保远程目录存在
            self.client.mkdir("certificate") 
            return
            remote_dir = os.path.dirname(remote_path)
            if remote_dir and not self.client.check(remote_dir):
                self.client.mkdir(remote_dir)    
            print(f"确保远程目录存在: {remote_dir}")
            # 上传文件
            self.client.upload_sync(remote_path="/dav", local_path=local_path)
            print(f"文件上传成功: {local_path} -> {remote_path}")
            return True
        except Exception as e:
            print(f"文件上传失败: {str(e)}")
            return False
    
    def delete_file(self, remote_path):
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
     # 创建客户端实例
    client = WebDAVClient()
    remote_file_ = f"/imemos/sqlBackup/{remote_file}"
    r=client.upload_file(local_file, remote_file_)
    if r:
        return remote_file_
    else :
        return None
   
        

def delFile(remote_file):
    # 删除文件示例
    client.delete_file("c/dl-file/sqlBackup/a.txt")
    return None


# 使用示例
if __name__ == "__main__":
    uploadFile("requirements.txt",__getSqlFileName())
   
    
   

