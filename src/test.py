import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backup.loop import main2 as backupMain2

backupMain2((True,"../local/memos_prod.db"))
