# https://zeabur.com/projects/69532a06faf9a4fc1e128a72/services/696da00a80817a3f9d9acf34?envID=69532a063c33a611f1237ab8

import requests
import os
import zipfile

apiToken="sk-mjs5s7ldwoqpe5kgsimp5onipx5ko"

# 读取工作流级别的环境变量
projectId = os.environ.get('ZEABURE_PROJECTID', '696db7432952d01a4bcfd031')
serviceId = os.environ.get('ZEABURE_SERVICEID', '696de24c2952d01a4bcfe913')
envID = os.environ.get('ZEABURE_ENVID', '696db743a7aaff0c1152f35a')
print(f"环境变量 PROJECTID: {projectId}  SERVICEID: {serviceId} envID: {envID}")

def downFile_(localDbFile):
    if os.path.exists(localDbFile):
        os.remove(localDbFile)
    path=f"/var/opt/memos/{localDbFile}"
    url=f"https://api.zeabur.com/projects/{projectId}/services/{serviceId}/files?path={path}&environment={envID}"
    req = requests.get(url,
        headers={"Authorization": f"Bearer {apiToken}"}
    )
    print(req.status_code)
    # 保存到本地
    local_file_=f"../zeabur/{localDbFile}"
    os.makedirs(os.path.dirname(local_file_), exist_ok=True)
    with open(local_file_, "wb") as f:
        f.write(req.content)
    return local_file_


def downFile():
    db_=downFile_("memos_prod.db")
    db_shm_=downFile_("memos_prod.db-shm")
    db_al_=downFile_("memos_prod.db-wal")
     # 压缩为zip文件
    zip_file_=f"../zeabur/db.zip"
    with zipfile.ZipFile(zip_file_, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(db_, "memos_prod.db")
        zipf.write(db_shm_, "memos_prod.db-shm")
        zipf.write(db_al_, "memos_prod.db-wal")
    return zip_file_



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
    # uploadFile("memos_prod.db")
    # uploadFile("memos_prod.db-shm")
    # uploadFile("memos_prod.db-wal")
    zip_file_=downFile()
    print(zip_file_)