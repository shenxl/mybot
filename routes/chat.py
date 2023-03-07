# -*- coding: utf-8 -*-
import json
from flask import request
from flask_restful import Resource
from app.replybot import ReplyBot, BotStatus
from logs.logger import Logger

logger = Logger(__name__)
class Chat(Resource):
    def get(self, key=None):
        return {"result": "ok"}

    
    def post(self, key=None):
        # 获取请求数据
        data = request.json
        # 创建 ReplyBot 对象并初始化
        logger.info(json.dumps(data))
        replybot = ReplyBot(data,key)
        reply = replybot.reply()
        message = ""
        if reply == BotStatus.REGISTRATION_FAILED:
            message = "注册失败"
        elif reply == BotStatus.PROCESSING:
            message = "正常消息处理"
        elif reply == BotStatus.REGISTERED:
            message = "注册成功"
        elif reply == BotStatus.UNREGISTERED:
            message = "机器人未注册"
        elif reply == BotStatus.CLEARALLCHATS:
            message = "对话全部清理"
        elif reply == BotStatus.REPLYERROR:
            message = f"OPENAI 调用发生错误：{replybot.replyMsg}"
        elif reply == BotStatus.REPLY:
            message = replybot.replyMsg                       
        # 返回响应数据
        return {"message": message}
