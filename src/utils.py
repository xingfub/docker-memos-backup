import os
import sys
import time;
from datetime import datetime

def __getSqlFileName():
    now_=datetime.now()
    time_ = now_.strftime('%Y%m%d-%H%M')
    ret_="{}.db".format(time_)
    return ret_