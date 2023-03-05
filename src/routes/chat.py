# -*- coding: utf-8 -*-
from flask import request
from flask_restful import Resource
from src.replybot import ReplyBot, BotStatus
from src.logs.logger import Logger

logger = Logger(__name__)
class Chat(Resource):
    def get(self):
        return {"result": "ok"}
    
    def post(self):
        # 获取请求数据
        data = request.json
        key = data.get('key')
        # 创建 ReplyBot 对象并初始化
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
        logger.info(message)
        return {"message": message}
