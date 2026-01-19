# https://zeabur.com/projects/69532a06faf9a4fc1e128a72/services/696da00a80817a3f9d9acf34?envID=69532a063c33a611f1237ab8

import requests
import os


apiToken="sk-mjs5s7ldwoqpe5kgsimp5onipx5ko"

# 读取工作流级别的环境变量
projectId = os.environ.get('ZEABURE_PROJECTID', '696db7432952d01a4bcfd031')
serviceId = os.environ.get('ZEABURE_SERVICEID', '696dcaee2952d01a4bcfda57')
envID = os.environ.get('ZEABURE_ENVID', '696db743a7aaff0c1152f35a')
print(f"环境变量 PROJECTID: {projectId}  SERVICEID: {serviceId} envID: {envID}")

def downFile():
    localDbFile="memos_prod.db"
    if os.path.exists(localDbFile):
        os.remove(localDbFile)
    path="/var/opt/memos/memos_prod.db"
    url=f"https://api.zeabur.com/projects/{projectId}/services/{serviceId}/files?path={path}&environment={envID}"
    req = requests.get(url,
        headers={"Authorization": f"Bearer {apiToken}"}
    )
    print(req.status_code)
    print(len(req.content))
    # 保存到本地
    with open(localDbFile, "wb") as f:
        f.write(req.content)
    return localDbFile


def uploadFile(localDbFile):
    try:
        # 构造完整的API URL
        url = f"https://api.zeabur.com/projects/{projectId}/services/{serviceId}/files"
        params = {
            "path": f"/var/opt/memos/{localDbFile}",
            "environment": envID
        }
        # 上传文件
        with open(localDbFile, "rb") as file:
            req = requests.post(
                url,
                data=params,
                headers={"Authorization": f"Bearer {apiToken}"},
                files={"file": file}
            )
        
        print(f"上传文件状态码: {req.status_code}")
        print(f"上传文件响应: {req.text}")
        
        # 检查上传是否成功
        if req.status_code in [200, 201, 204]:
            print(f"文件上传成功: {localDbFile} ")
            return True
        else:
            print(f"文件上传失败: HTTP {req.status_code}")
            return False
            
    except Exception as e:
        print(f"文件上传异常: {str(e)}")
        return False


if __name__ == "__main__":
    uploadFile("memos_prod.db")
    # uploadFile("memos_prod.db-shm")
    # uploadFile("memos_prod.db-wal")
    # downFile()