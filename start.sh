
# https://github.com/usememos/memos
# https://www.usememos.com/docs
# https://memos.apidocumentation.com/reference

# 获取脚本的绝对路径
script_path=$(readlink -f "$0")
# 获取脚本所在的目录
script_dir=$(dirname "$script_path")

docker run -d \
--name memos \
-p 5230:5230 \
--restart always \
-v $script_dir/.memos/:/var/opt/memos \
neosmemo/memos:stable
