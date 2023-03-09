from .executor import CommandStrategy
from dbs.bots import bots

class InitCommandStrategy(CommandStrategy):
    def execute(self,  command_arg):
        # TODO: 实现初始化机器人的逻辑，添加 bot 对象到数据库中
        username = self.rebot["userID"]
        return f"机器人{username}已初始化完成"