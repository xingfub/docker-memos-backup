#保存远程地址，每个保存5份超过的则删除
import requests
import json



password_="xin"
keyQiniu="memos_qiniu"
keyAlist="memos_alist"
keyJianguo="memos_jianguo"

url ="https://music.xingfub.dpdns.org"
# url="http://127.0.0.1:8787"

writeUrl=f"{url}/api/writeKey"
readUrl=f"{url}/api/readKey"

def writeKey_(key, value):
    res=requests.post(readUrl,
     json={"key": key,"password":password_})
    print(res.text)
    json_=res.json()
    print(f"readKey {key} {json_}")
    data_=[]
    if "data" in json_ :
        if   isinstance(json_["data"], list):
            data_=json_["data"]
        elif isinstance(json_["data"], str):
            try:
                data_=json.loads(json_["data"])
            except:
                pass
    data_.append(value)
    print(f"writeKey {key} {json.dumps(data_)}")
    neddDel=None
    if len(data_)>10:
       neddDel= data_.pop(0)
    res=requests.post(writeUrl,
    json={"key": key,"password":password_,"value":json.dumps(data_)})
    print(res.text)
    return neddDel

def writeKey(qiniu=None, alist=None,jianguo=None):
    d1=None
    d2=None
    d3=None
    if qiniu:
        d1=writeKey_(keyQiniu, qiniu)
    if alist:
        d2=writeKey_(keyAlist, alist)
    if jianguo:
        d3=writeKey_(keyJianguo, jianguo)
    return d1,d2,d3


