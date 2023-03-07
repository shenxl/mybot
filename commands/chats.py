from .executor import CommandStrategy

class ChatsCommandStrategy(CommandStrategy):
    def __init__(self):
        self.chat_queue = None
    
    # TODO: 实现对话逻辑
    
    def execute(self, command_arg):
        return str(self.chat_queue)
    
class ChatsClsCommandStrategy(CommandStrategy):
    def __init__(self):
        self.chat_queue = None #ChatQueue()
    
    def execute(self, command_arg):
        n = int(command_arg) if command_arg else len(self.chat_queue)
        self.chat_queue.clear(n)
        return f"清理了{n}个聊天记录"