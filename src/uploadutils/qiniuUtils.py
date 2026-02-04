# -*- coding: utf-8 -*
# 定时任务使用crontab -l 
# crontab -e
# 1 2 * * * python3 /home/ubuntu/light/memos/backsql.py > /home/ubuntu/light/memos/backsql.log 2>&1 &
import json
import os
import sys
import time;
from datetime import datetime
from qiniu import Auth, put_file, BucketManager

access_key = 'zy6LXacpmYdpGKPoS2RsVhRHB4Evmaxtlk9YyoXm'
secret_key = 'MhrZJoN_0zaB9qcHI4lQNc8MEc9uN_7n3FP3Lsz2'
bucket_name = 'xin-mysql'  # 要上传的空间
"""
上传到私有空间 sql备份数据
将上次上传的删掉
将本地的缓存文件删掉，只保存最新的7个
"""


def __getToken():
    """
    获取签名
    :return:
    """
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, expires=3600 * 24)
    return token




def uploadFile(localfile,remoteFileName):
    """
    上传文件
    :param localfile:
    :return:
    """
    # 要上传文件的本地路径
    if True:
        return None
    try:
        key_ = f"memosZeaburBack/{remoteFileName}" 
        print("key", key_)
        ret, info = put_file(__getToken(), key_, localfile)
        print(ret)
        print(info)
        return ret["key"]
    except Exception as err:
        print(err)


def __getUrl(fileName):
    """
    获取下载地址
    :param fileName:
    :return:
    """
    q = Auth(access_key, secret_key)
    # 有两种方式构造base_url的形式
    strs = ("yps-sql.aotbot.com", fileName)
    base_url = 'http://%s/%s' % strs
    private_url = q.private_download_url(base_url, expires=3600 * 24 * 30)
    return private_url


def delFile(key_):
    """
    从7牛中删除数据
    :param key_:
    :return:
    """
    print("delFile", key_)
    q = Auth(access_key, secret_key)
    bucket = BucketManager(q)
    ret, info = bucket.delete(bucket_name, key_)
    print(info)
    pass





