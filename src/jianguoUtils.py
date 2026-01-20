import requests
import os
from urllib.parse import urljoin

# 禁用SSL警告
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

class WebDAVClient:
    def __init__(self):
        self.webdav_hostname = 'https://dav.jianguoyun.com/dav'
        self.username = "proud2008@qq.com"
        self.password = "JIANGUOYUNhu0303"
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        self.session.verify = False  # 忽略SSL验证
    
    def _make_url(self, path):
        """
        构建完整的WebDAV URL
        """
        if not path.startswith('/'):
            path = '/' + path
        return urljoin(self.webdav_hostname, path.lstrip('/'))
    
    def check(self, remote_path):
        """
        检查远程路径是否存在
        """
        try:
            url = self._make_url(remote_path)
            response = self.session.request('PROPFIND', url)
            return response.status_code in [200, 207]
        except Exception as e:
            print(f"检查路径存在失败: {str(e)}")
            return False
    
    def mkdir(self, remote_path):
        """
        创建远程目录
        """
        try:
            url = self._make_url(remote_path)
            response = self.session.request('MKCOL', url)
            return response.status_code in [201, 301]
        except Exception as e:
            print(f"创建目录失败: {str(e)}")
            return False
    
    def upload_file(self, local_path, remote_path):
        try:
            if not os.path.exists(local_path):
                print(f"本地文件不存在: {local_path}")
                return False
            print(f"本地文件存在: {local_path}")
            
            # 确保远程目录存在
            remote_dir = os.path.dirname(remote_path)
            if remote_dir and remote_dir != '/':
                if not self.check(remote_dir):
                    if self.mkdir(remote_dir):
                        print(f"创建远程目录成功: {remote_dir}")
                    else:
                        print(f"创建远程目录失败: {remote_dir}")
                        return False
                print(f"远程目录存在: {remote_dir}")
            
            # 上传文件
            url = self._make_url(remote_path)
            with open(local_path, 'rb') as file:
                response = self.session.put(url, data=file)
            
            if response.status_code in [200, 201, 204]:
                print(f"文件上传成功: {local_path} -> {remote_path}")
                return True
            else:
                print(f"文件上传失败: HTTP {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"文件上传失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def delete_file(self, remote_path):
        try:
            # 检查文件是否存在
            if not self.check(remote_path):
                print(f"远程文件不存在: {remote_path}")
                return False
                
            # 删除文件
            url = self._make_url(remote_path)
            response = self.session.delete(url)
            
            if response.status_code in [200, 204]:
                print(f"文件删除成功: {remote_path}")
                return True
            else:
                print(f"文件删除失败: HTTP {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"文件删除失败: {str(e)}")
            import traceback
            traceback.print_exc()
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
    # 创建客户端实例
    client = WebDAVClient()
    remote_file_ = f"/imemos/sqlBackup/{remote_file}"
    r=client.delete_file(remote_file_)
    if r:
        return remote_file_
    else :
        return None


# 使用示例
if __name__ == "__main__":
    uploadFile("requirements.txt","requirements.txt")
   
    
   

