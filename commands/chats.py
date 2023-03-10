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
        title = "🤖 <font color='#404040'>清理完成</font>"
        info = "🗑️ 对话内容已经全部清理"
        message = {
            "msgtype": "markdown",
            "markdown": {
                "text": f"#### {title}  \n\n##### {info}"
            }
        }
        return (message, None) , BotStatus.CLEAR_ALL_CHATS