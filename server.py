import os
import sys
import argparse
import signal
import subprocess
from flask import Flask
from flask_restful import Api
from routes.chat import Chat

# 初始化 Flask 和 Flask-RESTful
app = Flask(__name__)
api = Api(app)

# 添加 Chat 资源到 Flask-RESTful
api.add_resource(Chat, '/chat', '/chat/<string:key>')

def start_server(bind, workers, log_path):
    """
    启动 Gunicorn 服务器
    """
    cmd = f"gunicorn server:app -w {workers} -b {bind} --access-logfile {log_path}"
    subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def stop_server():
    """
    停止 Gunicorn 服务器
    """
    with open("gunicorn.pid", "r") as f:
        pid = int(f.read())
    os.kill(pid, signal.SIGTERM)

def restart_server(bind, workers, log_path):
    """
    重启 Gunicorn 服务器
    """
    stop_server()
    start_server(bind, workers, log_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--bind', dest='bind', help='服务监听的 IP 和端口', default='0.0.0.0:8000')
    parser.add_argument('--workers', dest='workers', help='进程数', default=4, type=int)
    parser.add_argument('--log-path', dest='log_path', help='日志文件路径', default='/var/log/gunicorn/access.log')
    
    args = parser.parse_args()

    env = os.environ.get('ENV')
    if env != 'prod':
        app.run(debug=True)
    else:
        # 生产环境下使用 nohup 启动 Gunicorn 服务器并写入 pid 文件
        cmd = f"gunicorn server:app -w {args.workers} -b {args.bind}"
        pid_file = "gunicorn.pid"
        with open(pid_file, "w") as f:
            subprocess.Popen(f"nohup {cmd} >{args.log_path} 2>&1 &", shell=True, stdout=f)
