
# https://github.com/usememos/memos
# https://www.usememos.com/docs
# https://memos.apidocumentation.com/reference

# app版本 只支持到0.25.0版本 要指定版本
#https://github.com/mudkipme/MoeMemosAndroid/releases/latest
# 获取脚本的绝对路径
script_path=$(readlink -f "$0")
# 获取脚本所在的目录
script_dir=$(dirname "$script_path")

name="memos2"
port=3008
sudo docker stop $name
sudo docker rm $name
sudo docker run -d \
--name $name \
-p $port:5230 \
--restart always \
-v $script_dir/.memos2/:/var/opt/memos \
neosmemo/memos:0.25.0
