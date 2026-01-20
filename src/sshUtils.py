import paramiko
import os
import zipfile


class SSHClient:
    def __init__(self):
        """
        初始化SSH客户端
        
        Args:
            hostname (str): 服务器地址
            port (int): SSH端口，默认为22
            username (str): 用户名
            private_key_path (str): 私钥文件路径
        """
        self.hostname = "43.159.50.21"
        self.port = 22
        self.username = "ubuntu"
        self.private_key_path = "../linux/id_rsa"
        self.client = paramiko.SSHClient()
        # 自动添加未知主机的密钥
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    def connect(self):
        """
        连接到SSH服务器
        
        Returns:
            bool: 连接成功返回True，失败返回False
        """
        try:
            if self.private_key_path:
                # 使用私钥认证
                private_key = paramiko.RSAKey.from_private_key_file(self.private_key_path)
                self.client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    pkey=private_key)
            else:
                # 使用密码认证（如果需要）
                self.client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username)
            print(f"成功连接到SSH服务器: {self.username}@{self.hostname}:{self.port}")
            return True
        except Exception as e:
            print(f"SSH连接失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def download_file(self, remote_path, local_path):
        try:
            # 检查是否已连接
            if not self.client.get_transport() or not self.client.get_transport().is_active():
                print("SSH连接未建立，正在尝试连接...")
                if not self.connect():
                    return False
            
            # 创建SFTP客户端
            sftp = self.client.open_sftp()
            
            # 获取文件大小（可选，用于显示进度）
            remote_file_size = sftp.stat(remote_path).st_size
            print(f"开始下载文件: {remote_path}")
            print(f"文件大小: {remote_file_size} 字节")
            
            # 下载文件
            sftp.get(remote_path, local_path)
            
            # 关闭SFTP连接
            sftp.close()
            
            # 验证下载是否成功
            if os.path.exists(local_path) and os.path.getsize(local_path) == remote_file_size:
                print(f"文件下载成功: {local_path}")
                return True
            else:
                print(f"文件下载失败: 本地文件与远程文件大小不一致")
                return False
                
        except FileNotFoundError:
            print(f"文件下载失败: 远程文件不存在 - {remote_path}")
            return False
        except Exception as e:
            print(f"文件下载失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def upload_file(self, local_path, remote_path):
        """
        通过SFTP上传本地文件到服务器
        
        Args:
            local_path (str): 本地文件路径
            remote_path (str): 服务器端保存路径
            
        Returns:
            bool: 上传成功返回True，失败返回False
        """
        try:
            # 检查是否已连接
            if not self.client.get_transport() or not self.client.get_transport().is_active():
                print("SSH连接未建立，正在尝试连接...")
                if not self.connect():
                    return False
            
            # 检查本地文件是否存在
            if not os.path.exists(local_path):
                print(f"文件上传失败: 本地文件不存在 - {local_path}")
                return False
            
            # 创建SFTP客户端
            sftp = self.client.open_sftp()
            
            # 获取文件大小
            local_file_size = os.path.getsize(local_path)
            print(f"开始上传文件: {local_path}")
            print(f"文件大小: {local_file_size} 字节")
            
            # 上传文件
            sftp.put(local_path, remote_path)
            
            # 关闭SFTP连接
            sftp.close()
            
            print(f"文件上传成功: {remote_path}")
            return True
            
        except Exception as e:
            print(f"文件上传失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def close(self):
        """
        关闭SSH连接
        """
        try:
            if self.client.get_transport() and self.client.get_transport().is_active():
                self.client.close()
                print("SSH连接已关闭")
        except Exception as e:
            print(f"关闭SSH连接失败: {str(e)}")


def downFile():
      # 配置文件路径
    remote_file_path = "/home/ubuntu/light/memos/.memos/"  
    local_save_path="../ssh/"
    # 创建SSH客户端
    ssh = SSHClient()
    try:
        # 连接到服务器
        if ssh.connect():
            # 下载文件
            ssh.download_file(f"{remote_file_path}memos_prod.db", f"{local_save_path}memos_prod.db")
            ssh.download_file(f"{remote_file_path}memos_prod.db-shm", f"{local_save_path}memos_prod.db-shm")
            ssh.download_file(f"{remote_file_path}memos_prod.b-wal", f"{local_save_path}memos_prod.db-wal")
            # 上传文件示例（可选）
            # ssh.upload_file("local_file.txt", "/path/to/remote/upload.txt")
    finally:
        # 关闭连接
        ssh.close()
     # 压缩为zip文件
    zip_file_=f"{local_save_path}db_ssh.zip"
    with zipfile.ZipFile(zip_file_, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(f"{local_save_path}memos_prod.db", "memos_prod.db")
        zipf.write(f"{local_save_path}memos_prod.db-shm", "memos_prod.db-shm")
        zipf.write(f"{local_save_path}memos_prod.db-wal", "memos_prod.db-wal")
    return zip_file_

# 使用示例
if __name__ == "__main__":
    # 1、下载文件
    print("1.downFile")
    localDbFile=downFile()