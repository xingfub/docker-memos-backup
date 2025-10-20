
# https://github.com/usememos/memos
# https://www.usememos.com/docs
# https://memos.apidocumentation.com/reference

# 获取脚本的绝对路径
script_path=$(readlink -f "$0")
# 获取脚本所在的目录
script_dir=$(dirname "$script_path")

memosName="memos"
memosPort=5230
mortisName="mortis"
mortisPort=5231

sudo docker stop $memosName
sudo docker rm $memosName

sudo docker stop $mortisName
sudo docker rm $mortisName

sudo docker run -d \
  --name $memosName \
  -p $memosPort:5230 \
  --restart always \
  -v $script_dir/.memos/:/var/opt/memos \
  neosmemo/memos:0.25.1

sudo docker run -d \
  --name $mortisName \
  -p $mortisPort:5231 \
  --link memos:$memosName \
  --entrypoint "/app/mortis" \
  ghcr.io/mudkipme/mortis:0.25.1 \
  -grpc-addr=172.17.0.4:5230 -addr=0.0.0.0 -port=5231
  

