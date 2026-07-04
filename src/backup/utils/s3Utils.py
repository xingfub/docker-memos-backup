# 添加当前目录到Python路径
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import boto3
from botocore.exceptions import NoCredentialsError
import os
from api.config import load_history as loadHistory, save_history as saveHistory

class S3Client:
    def __init__(self,s3Config):
        """
        初始化S3客户端
        """
        self.s3 = boto3.client(
            's3',
            endpoint_url=s3Config['endpoint_url'],
            aws_access_key_id=s3Config['access_key'],
            aws_secret_access_key=s3Config['secret_key'],
            region_name=s3Config['region_name']  # 根据实际区域调整
        )
        self.Bucket_Name=s3Config['bucket']
    
    def upload_file(self, local_path, remote_path):
        """
        上传文件到S3存储
        
        Args:
            local_path (str): 本地文件路径
            remote_path (str): 远程文件路径（S3中的键）
            
        Returns:
            bool: 上传成功返回True，失败返回False
        """
        try:
            if not os.path.exists(local_path):
                print(f"本地文件不存在: {local_path}")
                return False,"本地文件不存在"
            
            # 上传文件
            self.s3.upload_file(local_path, self.Bucket_Name, remote_path)
            print(f"文件上传成功: {local_path} -> s3://{self.Bucket_Name}/{remote_path}")
            return True,remote_path
        except NoCredentialsError:
            print("S3凭证错误")
            return False,"S3凭证错误"
        except Exception as e:
            print(f"文件上传失败: {str(e)}")
            return False,str(e)
    
    def delete_file(self, remote_path):
        """
        从S3存储删除文件
        
        Args:
            remote_path (str): 远程文件路径（S3中的键）
            
        Returns:
            bool: 删除成功返回True，失败返回False
        """
        try:
            # 删除文件
            self.s3.delete_object(Bucket=self.Bucket_Name, Key=remote_path)
            print(f"文件删除成功: s3://{self.Bucket_Name}/{remote_path}")
            return True
        except NoCredentialsError:
            print("S3凭证错误")
            return False,"S3凭证错误"
        except Exception as e:
            print(f"文件删除失败: {str(e)}")
            return False,f"文件删除失败: {str(e)}"

# 便捷函数
def uploadFile(local_file, remote_file,s3Config):
    """
    上传文件到S3的便捷函数
    
    Args:
        local_file (str): 本地文件路径
        remote_file (str): 远程文件路径
        
    Returns:
        str: 上传后的S3路径
    """
    print(f"------s3-----")
    client = S3Client(s3Config)
    save_path = s3Config.get('save_path', '')
    if save_path:
        remote_file_ = f"{save_path}/{remote_file}" if not save_path.endswith('/') else f"{save_path}{remote_file}"
    else:
        remote_file_ = remote_file
    t=client.upload_file(local_file, remote_file_)
    return t

def delFile(remote_file,s3Config):
    """
    从S3删除文件的便捷函数
    
    Args:
        remote_file (str): 远程文件路径
    """
    client = S3Client(s3Config)
    client.delete_file(remote_file)


def main(localDbFile,remoteFileName,s3Config):
    """
    上传文件到WebDAV服务器,服务器的文件超过7天删除,返回是否执行成功
    Args:
        localDbFile (str): 本地文件路径
        remoteFileName (str): 远程文件名
    Returns:
        bool: 上传成功返回True，失败返回False
    """
    historyKey="s3"
    remote_file = uploadFile(localDbFile, remoteFileName,s3Config)
    if not remote_file[0]:
        return False
    history = loadHistory(historyKey)
    history.insert(0, remote_file[1])
    new_files = history[:7]
    saveHistory(historyKey,new_files)
    old_files = history[7:]
    # 删除超出7条的旧文件
    for old_file in old_files:
        if old_file:
            delFile(old_file,s3Config)
    return True
        
