from .executor import CommandStrategy
from dbs.chats import chats
class ChatsCommandStrategy(CommandStrategy):
    def __init__(self):
        self.chat_queue = None
    def execute(self, robot, command_arg):
        return str(self.chat_queue)
    
class ChatsClsCommandStrategy(CommandStrategy):
    def __init__(self):
        self.chat_queue = None #ChatQueue()
    
    def execute(self, robot, command_arg):
        chats.clear_by_userID(robot["userID"])