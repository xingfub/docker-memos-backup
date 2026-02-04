import boto3
from botocore.exceptions import NoCredentialsError
import os

Access_Key="plp4i1d0"
SecretKey="c84kql8qldjwmm4k"
Internal="object-storage.objectstorage-system.svc.cluster.local"
External="objectstorageapi.ap-southeast-1.clawcloudrun.com"
Bucket_Name="plp4i1d0-xinfub"  # 替换为实际的桶名称

class S3Client:
    def __init__(self):
        """
        初始化S3客户端
        """
        self.s3 = boto3.client(
            's3',
            endpoint_url=f"https://{External}",
            aws_access_key_id=Access_Key,
            aws_secret_access_key=SecretKey,
            region_name='ap-southeast-1'  # 根据实际区域调整
        )
    
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
                return False
            
            # 上传文件
            self.s3.upload_file(local_path, Bucket_Name, remote_path)
            print(f"文件上传成功: {local_path} -> s3://{Bucket_Name}/{remote_path}")
            return True
        except NoCredentialsError:
            print("S3凭证错误")
            return False
        except Exception as e:
            print(f"文件上传失败: {str(e)}")
            return False
    
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
            self.s3.delete_object(Bucket=Bucket_Name, Key=remote_path)
            print(f"文件删除成功: s3://{Bucket_Name}/{remote_path}")
            return True
        except NoCredentialsError:
            print("S3凭证错误")
            return False
        except Exception as e:
            print(f"文件删除失败: {str(e)}")
            return False

# 便捷函数
def uploadFile(local_file, remote_file):
    """
    上传文件到S3的便捷函数
    
    Args:
        local_file (str): 本地文件路径
        remote_file (str): 远程文件路径
        
    Returns:
        str: 上传后的S3路径
    """
    client = S3Client()
    client.upload_file(local_file, remote_file)
    return f"s3://{Bucket_Name}/{remote_file}"

def delFile(remote_file):
    """
    从S3删除文件的便捷函数
    
    Args:
        remote_file (str): 远程文件路径
    """
    client = S3Client()
    client.delete_file(remote_file)

if __name__ == "__main__":
    # 测试上传文件
    local_file = "main.py"
    remote_file = "test.txt"
    # uploadFile(local_file, remote_file)
    # 测试删除文件
    delFile(remote_file)