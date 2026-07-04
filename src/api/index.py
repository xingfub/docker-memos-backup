import os
import json
import time
import re
from flask import Blueprint, Config, request
from flask import  jsonify, session

from .config import load_config, save_config
from .config import  check_password, set_password
from .config import  has_password
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
        required = ['to_email']
        for key in required:
            if key not in params:
                return jsonify({'code': 400, 'message': f'{key} 不能为空'})
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', params['to_email']):
            return jsonify({'code': 400, 'message': '请输入有效的邮箱地址'})
        config['email'] = params
    elif backup_type == 'webdav':
        required = ['url', 'username', 'password']
        for key in required:
            if key not in params:
                return jsonify({'code': 400, 'message': f'{key} 不能为空'})
        if not re.match(r'^https?:\/\/[^\s]+$', params['url']):
            return jsonify({'code': 400, 'message': '请输入有效的URL地址'})
        config['webdav'] = params
    elif backup_type == 's3':
        required = ['endpoint_url', 'access_key', 'secret_key', 'bucket']
        for key in required:
            if key not in params:
                return jsonify({'code': 400, 'message': f'{key} 不能为空'})
        if not re.match(r'^https?:\/\/[^\s]+$', params['endpoint_url']):
            return jsonify({'code': 400, 'message': '请输入有效的Endpoint URL'})
        config['s3'] = params

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
    if restore_result:
        return jsonify({'code': 200, 'message': '恢复成功', 'filename': file.filename})
    return jsonify({'code': 400, 'message': '恢复失败'})
