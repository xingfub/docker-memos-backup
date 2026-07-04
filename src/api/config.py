import os
import json

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'history.json')


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)


def set_password(password):
    config = load_config()
    config['password'] = password
    save_config(config)


def check_password(password):
    config = load_config()
    stored_password = config.get('password', '')
    if not stored_password:
        return True
    return password == stored_password


def has_password():
    config = load_config()
    return 'password' in config and config['password']


def load_history(historyKey=None):
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            historyAll = json.load(f)
            if historyKey is None:
                return historyAll
            return historyAll.get(historyKey, [])
    return [] if historyKey else {}


def save_history(historyKey,history):
    historyAll = load_history()
    historyAll[historyKey] = history
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(historyAll, f, indent=2)
