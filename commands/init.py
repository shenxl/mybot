from .executor import CommandStrategy

class InitCommandStrategy(CommandStrategy):
    def execute(self, command_arg):
        # TODO: 实现初始化机器人的逻辑，添加 bot 对象到数据库中
        return "机器人已初始化完成"