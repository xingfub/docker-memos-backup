import os
import json
import time
import re
from flask import Blueprint, Config, request
from flask import  jsonify, session

from .config import load_config, save_config
from .config import  check_password, set_password
from .config import  has_password
from .config import load_history, save_history
from backup.index import restore_memos_db as restoreMemosDb
from backup.loop import  main as backupMemosDb



api_bp = Blueprint('api', __name__)


@api_bp.route('/check-password', methods=['POST'])
def check_password_api():
    data = request.get_json()
    password = data.get('password', '')
    if check_password(password):
        # session['authenticated'] = True
        return jsonify({'code': 200, 'message': '验证成功'})
    return jsonify({'code': 401, 'message': '密码错误'})


@api_bp.route('/has-password', methods=['GET'])
def has_password_api():
    _pd = has_password()
    return jsonify({'code': 200, 'has_password': 1 if _pd else 0})


@api_bp.route('/set-password', methods=['POST'])
def set_password_api():
    data = request.get_json()
    password = data.get('password', '')
    if not password:
        return jsonify({'code': 400, 'message': '密码不能为空'})
    set_password(password)
    return jsonify({'code': 200, 'message': '密码设置成功'})


@api_bp.route('/clear-password', methods=['POST'])
def clear_password_api():
    config = load_config()
    if 'password' in config:
        del config['password']
        save_config(config)
    return jsonify({'code': 200, 'message': '密码已清除'})


@api_bp.route('/backup', methods=['POST'])
def backup():
    print("backup request")
    data = request.get_json()
    backup_type = data.get('type', '')
    params = data.get('params', {})

    if backup_type not in ['email', 'webdav', 's3']:
        return jsonify({'code': 400, 'message': '无效的备份类型'})

    config = load_config()
    if backup_type == 'email':
        if params.get('to_email'):
            if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', params['to_email']):
                return jsonify({'code': 400, 'message': '请输入有效的邮箱地址'})
            config['email'] = params
        elif any(params.values()):
            return jsonify({'code': 400, 'message': '接收邮箱不能为空'})
        else:
            if 'email' in config:
                del config['email']
    elif backup_type == 'webdav':
        if params.get('url') and params.get('username') and params.get('password'):
            if not re.match(r'^https?:\/\/[^\s]+$', params['url']):
                return jsonify({'code': 400, 'message': '请输入有效的URL地址'})
            config['webdav'] = params
        elif any(params.values()):
            return jsonify({'code': 400, 'message': 'WebDAV地址、用户名和密码不能为空'})
        else:
            if 'webdav' in config:
                del config['webdav']
    elif backup_type == 's3':
        if params.get('endpoint_url') and params.get('access_key') and params.get('secret_key') and params.get('bucket'):
            if not re.match(r'^https?:\/\/[^\s]+$', params['endpoint_url']):
                return jsonify({'code': 400, 'message': '请输入有效的Endpoint URL'})
            config['s3'] = params
        elif any(params.values()):
            return jsonify({'code': 400, 'message': 'Endpoint URL、Access Key、Secret Key和Bucket不能为空'})
        else:
            if 's3' in config:
                del config['s3']

    save_config(config)
    type_labels = {'email': '邮件', 'webdav': 'WebDAV', 's3': 'S3'}
    return jsonify({'code': 200, 'message': f'{type_labels.get(backup_type, backup_type)} 配置保存成功'})


@api_bp.route('/backup/config', methods=['GET'])
def get_backup_config():
    config = load_config()
    return jsonify({
        'code': 200,
        'email': config.get('email', {}),
        'webdav': config.get('webdav', {}),
        's3': config.get('s3', {})
    })


@api_bp.route('/backup/run', methods=['POST'])
def run_backup():
   backup_result=backupMemosDb()
   return jsonify({'code': 200 if backup_result[0] else 400, 'message': backup_result[1]})


@api_bp.route('/restore', methods=['POST'])
def restore():
    if 'file' not in request.files:
        return jsonify({'code': 400, 'message': '请选择文件'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'code': 400, 'message': '请选择文件'})

    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)
    file.save(file_path)
    restore_result = restoreMemosDb(file_path)
    if restore_result[0]:
        return jsonify({'code': 200, 'message': restore_result[1], 'filename': file.filename})
    return jsonify({'code': 400, 'message': restore_result[1]})


@api_bp.route('/config/backup', methods=['GET'])
def config_backup():
    try:
        config_dir = os.path.dirname(os.path.dirname(__file__))
        config = load_config()
        history = load_history()
        backup_data = {
            'config': config,
            'history': history
        }
        return jsonify({'code': 200, 'data': backup_data})
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)})


@api_bp.route('/config/restore', methods=['POST'])
def config_restore():
    if 'file' not in request.files:
        return jsonify({'code': 400, 'message': '请选择文件'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'code': 400, 'message': '请选择文件'})
    if not file.filename.endswith('.json'):
        return jsonify({'code': 400, 'message': '只支持 .json 文件'})
    try:
        backup_data = json.load(file)
        if 'config' not in backup_data:
            return jsonify({'code': 400, 'message': '备份文件格式错误'})
        save_config(backup_data['config'])
        if 'history' in backup_data:
            save_history(history=backup_data['history'])
        return jsonify({'code': 200, 'message': '配置还原成功'})
    except json.JSONDecodeError:
        return jsonify({'code': 400, 'message': 'JSON 文件格式错误'})
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)})
