# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import logging
from flask import Flask
from flask_restful import Api
from flask_script import Manager
from routes.chat import Chat

# 初始化 Flask 和 Flask-RESTful
app = Flask(__name__)
api = Api(app)

# 添加 Chat 资源到 Flask-RESTful
api.add_resource(Chat, '/chat', '/chat/<string:key>')

# 配置日志记录
log_file = '/var/log/myapp.log'
if not os.path.exists(os.path.dirname(log_file)):
    os.makedirs(os.path.dirname(log_file))
handler = logging.FileHandler(log_file)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# 使用 Flask-Script 扩展管理应用程序
manager = Manager(app)

# 添加启动命令
@manager.command
def run():
    """启动服务器"""
    bind = '0.0.0.0:5000'
    workers = 4
    command = 'gunicorn -w {0} -b {1} app:app'.format(workers, bind)
    os.system('nohup {0} > /dev/null 2>&1 &'.format(command))

# 添加停止命令
@manager.command
def stop():
    """停止服务器"""
    command = 'killall gunicorn\n'
    os.system(command)

if __name__ == '__main__':

    env = os.environ.get('ENV')
    if env != 'prod':
        app.run(debug=True)
    else:
        manager.run()
