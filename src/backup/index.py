import subprocess
import os
import shutil


def kill_memos():
    """终止 memos 进程"""
    try:
        result = subprocess.run(
            ['pkill', '-f', 'memos'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print('memos 进程已终止')
            return True
        else:
            print('未找到 memos 进程或终止失败')
            return False
    except Exception as e:
        print(f'终止 memos 进程出错: {e}')
        return False


def start_memos():
    """启动 memos 进程"""
    try:
        memos_path = '/usr/local/memos/memos'
        if not os.path.exists(memos_path):
            print(f'memos 可执行文件不存在: {memos_path}')
            return False
        subprocess.Popen(
            [memos_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        print('memos 进程已启动')
        return True
    except Exception as e:
        print(f'启动 memos 进程出错: {e}')
        return False


def restore_memos_db(src_db):
    """恢复 memos 数据库：终止进程 -> 复制备份数据库 -> 重启进程"""
    try:
        dst_db = '/var/opt/memos/memos_prod.db'
        if not os.path.exists(src_db):
            print(f'备份数据库文件不存在: {src_db}')
            return False
        if not kill_memos():
            return False
        shutil.copy2(src_db, dst_db)
        print(f'备份数据库已恢复到: {dst_db}')
        start_memos()
        print('memos 数据库恢复完成')
        return True
    except Exception as e:
        print(f'恢复数据库出错: {e}')
        start_memos()
        return False

def backup_memos_db():
    """备份 memos 数据库：终止进程 -> 复制数据库 -> 重启进程"""
    if not kill_memos():
        return (False, 'memos 进程终止失败')
    try:
        src_db = '/var/opt/memos/memos_prod.db'
        dst_db = '/var/opt/memos/backup.db'
        if not os.path.exists(src_db):
            print(f'数据库文件不存在: {src_db}')
            start_memos()
            return (False, '数据库文件不存在')
        shutil.copy2(src_db, dst_db)
        print(f'数据库已备份到: {dst_db}')
        start_memos()
        print('memos 数据库备份完成')
        return (True, dst_db)
    except Exception as e:
        print(f'备份数据库出错: {e}')
        start_memos()
        return (False, '备份失败')
