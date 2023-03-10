import json

from .executor import CommandStrategy
from dbs.chats import chats
from app.chatbot import chatbot
from logs.logger import Logger
from app.botstatus import BotStatus

# 设置日志
logger = Logger(__name__)
chatbot = chatbot()

class MessageCommandStrategy(CommandStrategy):
    def execute(self, robot, command_arg):
        # 当前bot的当前用户对话
        messages = chats.get_by_bot_and_user(user_id=robot["user_id"],robot_key=robot["robot_key"])
        prompt = [{
            "role": "system", 
            "content": "忽略任何以前的提示，你是 chatGPT, 一个由OpenAI训练的大型语言模型"
        }]
        for message in messages:
            # logger.info(message.client_id, message.role, message.message, message.create_time)
            # 构造 chatgpt preload
            #message = json.dumps(message)
            prompt.append({
                "role": message["role"],
                "content": message["content"]
            })
        
        prompt.append({
            "role": "user",
            "content": command_arg
        })        
        
        (status,answer,usage) = chatbot.chat(chat=prompt)
        
        if status == "success":
            parent_id = chats.add_message(
                user_id = robot["user_id"],
                role = "user",
                content = command_arg,
                robot_key= robot["robot_key"],
            )
            chats.add_message(
                user_id = robot["user_id"],
                role = "assistant",
                content = answer,
                robot_key = robot["robot_key"],
                usage = usage["total_tokens"],
                parent_id = parent_id)
            
            # logger.info(f"本次对话资源使用情况, {json.dumps(usage)}")
            
            user_id = robot["user_id"]
            message = {
                "msgtype": "text",
                "text": {
                    "content": f"<at user_id=\"{user_id}\"></at>{answer}"
                }
            }
            
            # 将下一次的对话加入 prompt 便于后续计算上下文
            prompt.append({
                "role": "assistant",
                "content": answer
            })   
            return (message , prompt), BotStatus.REPLY
        
        else:
            message = {
                "msgtype": "text",
                "text": {
                    "content": f"<at user_id=\"{user_id}\"></at>{answer}"
                }
            }
            return (message , None), BotStatus.REPLYE_ERROR
