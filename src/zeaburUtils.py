# https://zeabur.com/projects/69532a06faf9a4fc1e128a72/services/696da00a80817a3f9d9acf34?envID=69532a063c33a611f1237ab8

import requests
import os


apiToken="sk-mjs5s7ldwoqpe5kgsimp5onipx5ko"

def downFile():
    localDbFile="memos_prod.db"
    if os.path.exists(localDbFile):
        os.remove(localDbFile)
    path="/var/opt/memos/memos_prod.db"
    req = requests.get(
        f"https://api.zeabur.com/projects/69532a06faf9a4fc1e128a72/services/696da00a80817a3f9d9acf34/files?path={path}&environment=69532a063c33a611f1237ab8",
        headers={"Authorization": f"Bearer {apiToken}"}
    )
    # 保存到本地
    with open(localDbFile, "wb") as f:
        f.write(req.content)
    return localDbFile


