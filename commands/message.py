import json
from itertools import chain

from .executor import CommandStrategy
from dbs.chats import Chats
from dbs.prompts import Prompts
from app.chatbot import chatbot
from logs.logger import Logger
from app.botstatus import BotStatus

# 设置日志
logger = Logger(__name__)
chatbot = chatbot()
chats = Chats()
prompts = Prompts()
class MessageCommandStrategy(CommandStrategy):
    def execute(self, robot, command_arg):
        # 当前bot的当前用户对话, 判断是否是以 act-> 开头
        chat_prompts = []
        if command_arg.startswith("act->"):
            print("进入扮演系统")
        else:
            print("进入对话系统")
            inter_prompts = prompts.get_systems_prompt()

            user_prompts = prompts.get_prompts(robot_key=robot["robot_key"])
            # TODO: 补充 channel 逻辑  
            summary_prompts = prompts.get_summary_prompt(robot_key=robot["robot_key"])
            # 将三个数组合并成一个并保持顺序
            chain_prompts = list(chain(inter_prompts, user_prompts, summary_prompts))
            for prompt in chain_prompts:
                chat_prompts.append({
                    "role": "system",
                    "content": prompt["content"]
                })

            messages = chats.get_chats(user_id=robot["user_id"],robot_key=robot["robot_key"])

            for message in messages:
                # logger.info(message.client_id, message.role, message.message, message.create_time)
                # 构造 chatgpt preload
                #message = json.dumps(message)
                chat_prompts.append({
                    "role": message["role"],
                    "content": message["content"]
                })
            
            chat_prompts.append({
                "role": "user",
                "content": command_arg
            })        
            
            (status,answer,usage) = chatbot.chat(chat=chat_prompts)
            
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
                chat_prompts.append({
                    "role": "assistant",
                    "content": answer
                })   
                return (message , chat_prompts), BotStatus.REPLY
            
            else:
                message = {
                    "msgtype": "text",
                    "text": {
                        "content": f"<at user_id=\"{user_id}\"></at>{answer}"
                    }
                }
                return (message , None), BotStatus.REPLYE_ERROR
