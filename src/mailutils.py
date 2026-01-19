# 发送邮件
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header

class EmailSender:
    def __init__(self, receiver_email="proud2008@qq.com"):
        """
        初始化邮件发送器
        
        Args:
            smtp_server (str): SMTP服务器地址
            smtp_port (int): SMTP服务器端口
            sender_email (str): 发件人邮箱
            sender_password (str): 发件人密码或授权码
            receiver_email (str): 收件人邮箱
        """
        self.smtp_server = "smtp.126.com"
        self.smtp_port = 25
        self.sender = "proud2008@126.com"
        self.password = "MXjXbLz7XejAyiLR"
        self.receiver = receiver_email
    
    def send_email(self, subject="zeaburBackup", body="zeaburBackup", file_path=None):
        """
        发送邮件
        
        Args:
            subject (str): 邮件主题
            body (str): 邮件正文
            file_paths (list, optional): 附件文件路径列表，默认为None
            
        Returns:
            bool: 发送成功返回True，失败返回False
        """
        try:
            # 创建一个MIMEMultipart对象
            msg = MIMEMultipart()
            msg['From'] = self.sender
            msg['To'] = self.receiver
            msg['Subject'] = Header(subject, 'utf-8')
            
            # 添加邮件正文
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # 添加附件
            if file_path:
                if os.path.exists(file_path):
                    # 获取文件名
                    file_name = os.path.basename(file_path)
                    
                    # 创建附件对象
                    with open(file_path, 'rb') as f:
                        attachment = MIMEApplication(f.read(), _subtype='octet-stream')
                        attachment.add_header('Content-Disposition', 'attachment', filename=Header(file_name, 'utf-8').encode())
                        msg.attach(attachment)
                    print(f"添加附件成功: {file_name}")
                else:
                    print(f"附件文件不存在: {file_path}")
            
            # 发送邮件
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                # 登录SMTP服务器
                server.login(self.sender, self.password)
                # 发送邮件
                server.send_message(msg)
            
            print("邮件发送成功")
            return True
            
        except Exception as e:
            print(f"邮件发送失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

def uploadFile(localDbFile):
    email_sender = EmailSender()
    # 发送邮件
    email_sender.send_email(file_path=localDbFile)

# 使用示例
if __name__ == "__main__":
    uploadFile("../zeabur/db.zip")
   