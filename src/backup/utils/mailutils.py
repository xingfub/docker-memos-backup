# 添加当前目录到Python路径
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import requests



def main(localDbFile,remoteFileName,config):
    to_email = config['to_email']
    try:
        with open(localDbFile, 'rb') as f:
            files = {'file': (remoteFileName, f)}
            data = {'recipient': to_email, 'subject': 'Memos备份',"senderName":"Memos","content":"备份文件已发送"}
            resp = requests.post('https://tools.xingfub.dpdns.org/xingfub/mail', 
            data=data, files=files, timeout=30000)
            print(f"邮件发送状态: {resp.status_code}")
            print(f"邮件发送响应: {resp.text}")
            return resp.status_code == 200
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False
    
