#  任务名称
#  name: script name
#  定时规则
#  cron: 1 9 * * *
import requests
import json
import datetime
import os

def send_post_json_request(domain_name,expiry_date,remaining_days):
    try:
        # 默认请求头
        default_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        # 默认数据
        data = {
                "password": "xin",
                "recipient": "proud2008@qq.com",
                "subject": "域名到期提醒",
                "message": f"域名{domain_name}到期日期为{expiry_date}，距离到期还有{remaining_days}天",
            }
        
        # 发送请求
        response = requests.post("http://mail.xingfub.dpdns.org", 
        json=data,headers=default_headers, timeout=360)
        # 尝试解析JSON响应
        return response.json()
    except Exception as e:
        print(f"请求失败: {e}")
        return {'error': str(e)}


def get_domain_expire_date(domain_name):
    try:
        # 构建URL
        url = f"https://dash.domain.digitalplat.org/whois?name={domain_name}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 QuarkPC/6.3.5.725'
        }
        # 发送GET请求
        response = requests.get(url, timeout=60, headers=headers)
        # 解析JSON响应
        data = response.text
        print(data)
        # 提取到期日期
        for line in data.split("\n"):
            if line.startswith("Registry Expiry Date"):
                print(line)
                expire_date_str = line.split(":")[1].strip()
                return expire_date_str
    except Exception as e:
        print(f"获取域名到期日期失败: {e}")
        return None
def calculate_days_until(target_date_str):
    try:
        # 解析目标日期
        target_date = datetime.datetime.strptime(target_date_str, '%Y-%m-%d')
        # 获取当前日期
        today = datetime.datetime.now()
        # 计算差值
        delta = target_date - today
        return delta.days
        
    except Exception as e:
        print(f"计算失败: {e}")
        return None

def main():
    date_=os.environ["xingfub"] 
    print(f"目标日期: {date_}")
    days_until = calculate_days_until(date_)
    print(f"距离 {date_} 还有 {days_until} 天")
    if days_until<30:
        send_post_json_request(date_)
    
if __name__ == "__main__":
    domain_name='xingfub.dpdns.org'
    expire_date = get_domain_expire_date(domain_name)
    if expire_date is None:
        print( f"无法获取域名{domain_name}到期日期,程序退出")
        exit(1)
    print(f"域名 {domain_name} 的到期日期是: {expire_date}")
    days_until = calculate_days_until(expire_date)
    print(f"距离 {expire_date} 还有 {days_until} 天")
    if days_until > 90:
        print("不需要发送邮件提醒,程序退出")
        exit(1)
    t=send_post_json_request(domain_name,expire_date,days_until)
    print(t)
