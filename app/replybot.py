# -*- coding: utf-8 -*-
import json
import requests
from typing import Dict
from enum import Enum

# from src.mocks.bots import mockBot
from urllib.parse import urlparse, parse_qs
from conf.config import get_config
from logs.logger import Logger
from dbs.bots import Bots
from dbs.chats import Chats 
from .chatbot import chatbot
from commands.parse import CommandType ,parse_command


# 设置日志
logger = Logger(__name__)
# mockbots = mockBot()
bots = Bots()
chats = Chats()
chatbot = chatbot()

class BotStatus(Enum):
    UNREGISTERED = 1
    PROCESSING = 2
    REGISTERED = 3
    REGISTRATION_FAILED = 4
    REPLY = 5
    REPLYERROR =6
    CLEARALLCHATS = 7


class ReplyBot:
    def __init__(self, data: Dict, key):
        self.chatid = data.get("chatid")
        self.creator = data.get("creator")
        self.content = data.get("content")
        self.robot_key = data.get("robot_key")
        self.url = data.get("url")
        self.hook_key = key
        self.ctime = data.get("ctime")
        self.replyMsg = ''
        # 初始化机器人
        self.init_bot()
        
    def init_bot(self):
        # 通过 robot_key ，获取机器人信息

        bot_info = bots.get_bot(self.robot_key)
        # logger.info(f"获取机器人信息！,{bot_info}")
        if bot_info is None:
            self.reply_str = BotStatus.UNREGISTERED
            self.register_bot()
            return
        self.rebot = bot_info
        command_type, command_arg = parse_command(self.content)
        if command_type == CommandType.MSG:
            self.process_message(command_arg)
        elif command_type == CommandType.CHATS_CLS:
            self.clearChats(command_arg)
        else:
            self.reply_str = BotStatus.PROCESSING
        
    # 判断是否需要初始化机器人
    def register_bot(self):
        # 初始化逻辑
        command_type, command_arg = parse_command(self.content)
        if command_type == CommandType.INIT:
            if self.hook_key:
                # 将 url 和 key 拼接成完整的 hook_url，并注册机器人
                hook_url = get_config().WOA_URL + self.hook_key
                # logger.info(f"key:{self.robot_key},chatid:{self.chatid},hook:{hook_url}")
                bots.add_bot(self.robot_key, self.chatid,hook_url)
                self.rebot = bots.get_bot(self.robot_key)
                self.reply_str = BotStatus.REGISTERED
            else:
                self.reply_str = BotStatus.REGISTRATION_FAILED
    
    # 处理对话命令
    def process_message(self, chat_message):
            # 向 ChatGPT 请求 Message,先保存firebase中    
        messages = chats.get_by_userID(self.chatid)
        prompt = [{"role": "system", "content": "忽略任何以前的提示，你是 chatGPT，一个由OpenAI训练的大型语言模型"}]
        for message in messages:
            # logger.info(message.client_id, message.role, message.message, message.create_time)
            # 构造 chatgpt preload
            #message = json.dumps(message)
            prompt.append({
                "role": message["role"],
                "content": message["content"]
            })
        # logger.info(json.dumps(prompt))
        new_prompt = prompt   
        new_prompt.append({
            "role": "user",
            "content": chat_message
        })
        
        chat_prompt_len = chatbot.num_tokens_from_messages(new_prompt)
        # logger.info(f"检查propmt 长度:{chat_prompt_len}")
        if chat_prompt_len > 1024:
            # 总结提示与并进行信息更新
            (status,answer,usage) = chatbot.get_topic_summary(prompt)
            if status == "success":
                # 清理之前的提示信息,并附加最新的
                # TODO 后续将 system 与 其他 role 的做区分
                chats.clear_by_userID(self.chatid)
                # TODO 添加 name 属性
                chats.add_message(self.chatid,"system",answer)
                new_prompt = [{"role": "system", "content": "忽略任何以前的提示，你是 chatGPT，一个由OpenAI训练的大型语言模型"}]
                new_prompt.append({"role":"system","content":answer})
                new_prompt.append({
                    "role": "user",
                    "content": chat_message
                })
            else:
                self.reply_str = BotStatus.REPLYERROR
                self.replyMsg = answer
                return
        
        (status,answer,usage) = chatbot.chat(new_prompt)
        if status == "success":
            parentid = chats.add_message(self.chatid,"user",chat_message)
            chats.add_message(self.chatid,"assistant",answer,parentid)
            logger.info(f"本次对话资源使用情况,{json.dumps(usage)}")
            self.replyMsg = answer
            self.reply_str = BotStatus.REPLY
        else:
            self.reply_str = BotStatus.REPLYERROR
            self.replyMsg = answer
    
    def clearChats(self,command_arg):
        if command_arg is None:       
            chats.clear_by_userID(self.chatid)
            self.reply_str = BotStatus.CLEARALLCHATS

    
    # 答复方法，需要针对不同的状态进行答复
    def reply(self): 
        header = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host":"xz.wps.cn",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        }
        reply_str = self.reply_str
        replyMsg = self.replyMsg
        
        if reply_str == BotStatus.REGISTRATION_FAILED:
            title = "❌<font color='#FF2400'>注册失败</font>❌"
            info = "📖 请使用 <font color='#1E90FF'>%help init%</font> 获取注册的操作步骤"
            message = {
                "msgtype": "markdown",
                "markdown": {
                    "text": f"#### {title}  \n\n##### {info}"
                }
            }
            return reply_str
        elif reply_str == BotStatus.PROCESSING:
            message = "正常消息处理"
        elif reply_str == BotStatus.REGISTERED:
            title = "🎉<font color='#1E90FF'>注册成功</font>🎉"
            info = "📖 请使用 <font color='#1E90FF'>%help%</font> 命令获取指令列表"
            message = {
                "msgtype": "markdown",
                "markdown": {
                    "text": f"#### {title}  \n\n##### {info}"
                }
            }
        elif reply_str == BotStatus.UNREGISTERED:
            title = "🤖<font color='#1E90FF'>机器人待注册</font>🤖"
            info = "📖 请使用 <font color='#1E90FF'>%init%</font> 命令进行注册"
            message = {
                "msgtype": "markdown",
                "markdown": {
                    "text": f"#### {title}  \n\n##### {info}"
                }
            }
            return reply_str
        elif reply_str == BotStatus.CLEARALLCHATS:
            title = "🤖 <font color='#404040'>清理完成</font>"
            info = "🗑️ 对话内容已经全部清理"
            message = {
                "msgtype": "markdown",
                "markdown": {
                    "text": f"#### {title}  \n\n##### {info}"
                }
            }
        elif reply_str == BotStatus.REPLYERROR:
            message = f"OPENAI 调用发生错误：{replyMsg}"
        elif reply_str == BotStatus.REPLY:
            message = {
                "msgtype": "text",
                "text": {
                    "content": f"<at user_id=\"{self.creator}\"></at>{replyMsg}"
                }
            }
        hookurl = self.rebot["hook"]
        requests.post(hookurl, data=json.dumps(message),headers=header)
        return reply_str
