from .executor import CommandStrategy
from dbs.chats import Chats
from app.botstatus import BotStatus
chats = Chats()
class ChatsCommandStrategy(CommandStrategy):
    def __init__(self):
        self.chat_queue = None
    def execute(self, robot, command_arg):
        return str(self.chat_queue)
    
class ChatsClsCommandStrategy(CommandStrategy):
    def __init__(self):
        self.chat_queue = None #ChatQueue()
    
    def execute(self, robot, command_arg):
        chats.clear_by_robot(robot_key=robot["robot_key"])
        message = {
            "msgtype": "markdown",
            "markdown": {
                "text": f"指令设置错误，请保持格式%instrs set 指令名称 指令描述%"
            }
        }
        return (message, None) , BotStatus.CLEAR_ALL_CHATS