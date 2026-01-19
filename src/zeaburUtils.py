# https://zeabur.com/projects/69532a06faf9a4fc1e128a72/services/696da00a80817a3f9d9acf34?envID=69532a063c33a611f1237ab8

import requests
import os


apiToken="sk-mjs5s7ldwoqpe5kgsimp5onipx5ko"

# 读取工作流级别的环境变量
projectId = os.environ.get('ZEABURE_PROJECTID', '696db7432952d01a4bcfd031')
serviceId = os.environ.get('ZEABURE_SERVICEID', '696db7542952d01a4bcfd032')
envID = os.environ.get('ZEABURE_ENVID', '696db743a7aaff0c1152f35a')
print(f"环境变量 PROJECTID: {projectId}  SERVICEID: {serviceId} envID: {envID}")

def downFile():
    localDbFile="memos_prod.db"
    if os.path.exists(localDbFile):
        os.remove(localDbFile)
    path="/var/opt/memos/memos_prod.db"
    # path="/var/opt/memos/aa.txt"
    req = requests.get(
        f"https://api.zeabur.com/projects/{projectId}/services/{serviceId}/files?path={path}&environment={envID}",
        headers={"Authorization": f"Bearer {apiToken}"}
    )
    print(req.status_code)
    print(len(req.content))
    # 保存到本地
    with open(localDbFile, "wb") as f:
        f.write(req.content)
    return localDbFile



if __name__ == "__main__":
    downFile()