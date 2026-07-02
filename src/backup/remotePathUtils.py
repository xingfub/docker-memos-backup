#保存远程地址，每个保存5份超过的则删除
import json
import os

output_file="../sqlback/config.json"

keyQiniu="qiniu"
keyAlist="alist"
keyJianguo="jianguo"


def readConfig():
    if not os.path.exists(output_file):
        return {}
    with open(output_file, "r") as f:
        data = json.load(f)
        return data

def writeConfig(data):
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

def writeKey_(config, key,value):
    if key not in config:
        data_=[]
    else:
        data_=config[key]
    data_.append(value)
    neddDel=None
    if len(data_)>10:
       neddDel= data_.pop(0)
    config[key]=data_
    return neddDel

def writeKey(s3Key=None, alist=None,jianguo=None):
    config=readConfig()
    d1=writeKey_(config,keyQiniu,s3Key)
    d2=writeKey_(config,keyAlist,alist)
    d3=writeKey_(config,keyJianguo,jianguo)
    writeConfig(config)
    return d1,d2,d3


