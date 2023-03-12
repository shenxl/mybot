# -*- coding: utf-8 -*-
import json
from flask import request
from flask_restful import Resource
from app.replybot import replyBot
from app.chatbot import chatbot
from app.botstatus import BotStatus
from logs.logger import Logger

from dbs.chats import Chats
from dbs.prompts import Prompts


# 加载策略
from commands.executor import CommandExecutor
from commands.chats import ChatsClsCommandStrategy
from commands.init import InitCommandStrategy
from commands.instrs import InstrsCommandStrategy, InstrsSetCommandStrategy, InstrsClsCommandStrategy
from commands.executor import RekeyCommandStrategy
from commands.executor import HelpCommandStrategy
from commands.parse import CommandType
from commands.message import MessageCommandStrategy


executor = CommandExecutor()
executor.add_strategy(CommandType.CHATS_CLS, ChatsClsCommandStrategy())
executor.add_strategy(CommandType.INIT, InitCommandStrategy())
# self.executor.add_strategy(CommandType.INSTRS, InstrsCommandStrategy())
executor.add_strategy(CommandType.INSTRS_SET, InstrsSetCommandStrategy(executor))
# self.executor.add_strategy(CommandType.INSTRS_CLS, InstrsClsCommandStrategy())
executor.add_strategy(CommandType.REKEY, RekeyCommandStrategy())
executor.add_strategy(CommandType.MSG, MessageCommandStrategy())
executor.add_strategy(CommandType.HELP, HelpCommandStrategy(executor))

executor.set_instruction_desc(CommandType.HELP,"输入%help%, 显示所有指令列表。")
executor.set_instruction_desc(CommandType.INIT,"输入%init%, 初始化机器人。**必须在回调中附加send key**")
executor.set_instruction_desc(CommandType.INSTRS_SET,"输入%instrs set >指令名< 指令描述%, 设置指令。")


logger = Logger(__name__)
chatbot = chatbot()
chats = Chats()
prompts = Prompts()
class Chat(Resource):
    def get(self, key):
        return {"result": "ok"}

    
    def post(self, key):
        # 获取请求数据
        data = request.json
        # 创建 ReplyBot 对象并初始化
        replybot = replyBot(data, key)
        content = replybot.content
        
        # try:
        # # 执行策略
        #     (message, paylopad), status = executor.execute(replybot, content)
        # except Exception as e:
        #     message = {
        #             "msgtype": "text",
        #             "text": {
        #                 "content": f"{e}"
        #             }
        #         }
        #     status = BotStatus.Exception
        #     paylopad = e
        # # 进行答复
        
        
        # # 执行策略
        (message, paylopad), status = executor.execute(replybot, content)
        replybot.reply(message)
        
        
        # 进行 prompt 压缩, 放置在 答复后进行
        if status == BotStatus.REPLY:
            prompt = paylopad
            tokens = chatbot.num_tokens_from_messages(prompt)
            if tokens > 20 :
                (status, answer, usage) = chatbot.get_topic_summary(prompt)
                if status == "success":
                    # 清理之前的提示信息,并附加最新的
                    # TODO 后续将 system 与 其他 role 的做区分
                    chats.clear_by_robot(robot_key=replybot.robot_key)
                    prompts.add_prompt(
                        create_tag = replybot.user_id,
                        catagory = "summary",
                        promot = answer,
                        robot_key = replybot.robot_key 
                    )
                    # chats.add_message(
                    #     user_id = "summary",
                    #     role = "system",
                    #     content = answer,
                    #     robot_key = replybot.robot_key,
                    #     usage = usage["total_tokens"]
                    #     )
                    status = BotStatus.COMPRESSED
                else:
                    status = BotStatus.COMPRESSION_FAILED
                    return
        
        message = ""
        
        if status == BotStatus.REGISTRATION_FAILED:
            message = "注册失败"
        elif status == BotStatus.PROCESSING:
            message = "正常消息处理"
        elif status == BotStatus.COMPRESSED:
            message = "已压缩"
        elif status == BotStatus.COMPRESSION_FAILED:
            message = "压缩失败"            
        elif status == BotStatus.REGISTERED:
            message = "注册成功"
        elif status == BotStatus.UNREGISTERED:
            message = "机器人未注册"
        elif status == BotStatus.CLEAR_ALL_CHATS:
            message = "对话全部清理"
        elif status == BotStatus.REPLY_ERROR:
            message = "OPENAI 调用发生错误"
        elif status == BotStatus.REPLY:
            message = "对话正常应答"
        elif status == BotStatus.HOOKKEY_NONE:
            message = "机器人未注册HookKEY"
        elif status == BotStatus.HELP_LIST:
            message = "帮助列表" 
        elif status == BotStatus.INSTRS_SET_SUCCESS:
            message = "指令设置成功"
        elif status == BotStatus.INSTRS_SET_FAILED:
            message = "指令设置失败"               
        elif status == BotStatus.Exception:
            message = f"出现异常 {paylopad}"                
        # 返回响应数据
        return {"message": message}
