from .parse import CommandType,parse_command
from app.botstatus import BotStatus

class CommandExecutor:
    def __init__(self):
        # CommandType 是一个枚举类，表示命令的类型，并且 `NullCommandStrategy` 是该命令类型的默认策略
        self.strategies = {command_type: NullCommandStrategy() for command_type in CommandType}
        self.instruction_desc = {command_type: '' for command_type in CommandType}
        self.instruction_example = {command_type: '' for command_type in CommandType}

    def add_strategy(self, command_type, command_strategy):
        self.strategies[command_type] = command_strategy

    def set_instruction_desc(self, command_type, desc):
        self.instruction_desc[command_type] = desc

    def set_instruction_example(self, command_type, example):
        self.instruction_example[command_type] = example

    def execute_command(self, robot, command_type, command_arg=None):
        return self.strategies[command_type].execute(robot, command_arg)

    def execute(self, robot, input_str, **kwargs):
        command_type, command_arg = parse_command(input_str)
        return self.execute_command(robot, command_type, command_arg, **kwargs)

"""
# 这段代码是面向对象编程中使用了抽象类、继承和多态的代码实例。
# 首先定义了一个抽象基类 `CommandStrategy`，其中包含一个未实现的 `execute` 方法，
# 这个方法在子类中将被实现。由于这个类中含有未实现的方法，因此它是一个抽象类，不能直接被实例化。
# 
# 其次，定义了一个子类 `NullCommandStrategy` 继承自 `CommandStrategy`
# 并给出了具体的实现。这个类中重写了 `execute` 方法，使其返回 None。
# 由于这个类中实现了 `execute` 方法，因此它是一个具体类，可以被实例化并使用。
# 
# 这样的好处是，通过定义一个抽象基类 `CommandStrategy`，可以规范所有的子类都必须实现 `execute` 方法，
# 而 `NullCommandStrategy` 继承了抽象基类的规范，并给出了具体的实现方法，使得代码可读性更好，
# 并且可以方便地扩展新的子类。
# 而在使用时，通过调用 `CommandStrategy` 类型的变量，
# 可以多态地调用 `execute` 方法，实现不同子类的行为差异，
# 并且将实现细节与主程序分离，提高代码的可维护性。
#
# """

class CommandStrategy:
    def execute(self, robot, command_arg):
        raise NotImplementedError

class NullCommandStrategy(CommandStrategy):
    def execute(self, robot, command_arg):
        return None

# 帮助指令
class HelpCommandStrategy(CommandStrategy):
    def __init__(self, executor):
        self.executor = executor

    def execute(self, robot, command_arg):
        if command_arg:
            # 显示指定指令的描述信息
            command_type = CommandType[command_arg.upper()]
            return self.executor.instruction_desc[command_type]
        else:
            # 显示所有指令的描述信息
            desc_list = [f"- <font color='#FF0000'>**{command_type.name.lower()}**</font> 指令 - {self.executor.instruction_desc[command_type]}"
                        for command_type in CommandType if self.executor.instruction_desc[command_type]]
            title = "📖<font color='#1E90FF'>帮助</font>"
            info = "\n\n".join(desc_list)
            message = {
                "msgtype": "markdown",
                "markdown": {
                    "text": f"#### {title}  \n\n {info}"
                }
            }
            return (message , None), BotStatus.HELP_LIST

class RekeyCommandStrategy(CommandStrategy):
    def execute(self, robot, command_arg):
        # TODO: 实现秘钥更换的逻辑
        username = robot["userID"]
        return f"{username}秘钥更换完成"


class UnknownCommandStrategy(CommandStrategy):
    def execute(self, robot, command_arg):
        return "无法识别的指令"


