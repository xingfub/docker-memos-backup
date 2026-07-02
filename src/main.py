import sys
import os
import threading
import time
import importlib.util
import pkgutil

if not hasattr(pkgutil, 'get_loader'):
    def get_loader(name):
        if name == '__main__':
            return None
        try:
            spec = importlib.util.find_spec(name)
            return spec.loader if spec else None
        except ValueError:
            return None
    pkgutil.get_loader = get_loader

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def create_app():
    from flask import Flask
    app = Flask(__name__, static_folder='public', static_url_path='/public')

    from api.index import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def index():
        with open(os.path.join(os.path.dirname(__file__), 'public', 'index.html'), 'r', encoding='utf-8') as f:
            return f.read()

    return app


def run_loop():
    while True:
        try:
            print("Loop running...")
        except Exception as e:
            print(f"Loop error: {e}")
        time.sleep(60)


if __name__ == "__main__":
    try:
        loop_thread = threading.Thread(target=run_loop, daemon=True)
        loop_thread.start()

        app = create_app()
        print("App created successfully")
        app.run(host='0.0.0.0', port=3000, debug=True)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()