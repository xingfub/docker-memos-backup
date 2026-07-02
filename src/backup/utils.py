import os
import sys
import time;
from datetime import datetime

def getRemoteFileName(localDbFile):
    now_=datetime.now()
    time_ = now_.strftime('%Y%m%d-%H%M')
    # 获取localDbFile的扩展名
    _, ext = os.path.splitext(localDbFile)
    ret_="{}{}".format(time_, ext)
    return ret_