# https://zeabur.com/projects/69532a06faf9a4fc1e128a72/services/696da00a80817a3f9d9acf34?envID=69532a063c33a611f1237ab8

import requests
import os


apiToken="sk-mjs5s7ldwoqpe5kgsimp5onipx5ko"

# 读取工作流级别的环境变量
serviceId = os.environ.get('SERVICEID', '696db2e980817a3f9d9ad5de')
print(f"环境变量 SERVICEID: {serviceId}")

def downFile():
    localDbFile="memos_prod.db"
    if os.path.exists(localDbFile):
        os.remove(localDbFile)
    path="/var/opt/memos/memos_prod.db"
    req = requests.get(
        f"https://api.zeabur.com/projects/69532a06faf9a4fc1e128a72/services/{serviceId}/files?path={path}&environment=69532a063c33a611f1237ab8",
        headers={"Authorization": f"Bearer {apiToken}"}
    )
    # 保存到本地
    with open(localDbFile, "wb") as f:
        f.write(req.content)
    return localDbFile


