import os
def doMemos(stop):
    if stop:
        os.system("sudo docker stop memos")
    else:
        os.system("sudo docker start memos")