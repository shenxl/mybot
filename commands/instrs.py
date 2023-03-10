from .executor import CommandStrategy, CommandType
from dbs.prompts import Prompts
from logs.logger import Logger
from app.botstatus import BotStatus

# 设置日志
logger = Logger(__name__)

prompts = Prompts()

# TODO： 思考指令相关的逻辑
class InstrsCommandStrategy(CommandStrategy):
    def __init__(self, robot, executor):
        self.executor = executor
        
    def execute(self, command_arg):
        if command_arg:
            # 显示指定指令的使用示例
            command_type = CommandType[command_arg.upper()]
            return self.executor.instruction_example[command_type]
        else:
            # 显示所有指令的使用示例
            example_list = [f"{command_type.name.lower()} - {self.executor.instruction_example[command_type]}"
                            for command_type in CommandType if self.executor.instruction_example[command_type]]
            return "\n".join(example_list)


        
class InstrsSetCommandStrategy(CommandStrategy):
    def __init__(self, executor):
        self.executor = executor

    def execute(self, robot, command_arg):
        parts = command_arg.split(maxsplit=1)
        if len(parts) > 1:
            instrs_name = parts[0].lower()
            instrs_content = parts[0].lower()
            des = "ts"
            
            title = "🤖 <font color='#404040'>指令设置完成</font>"
            info = f"- ⌨️指令{instrs_name}已经设置完成，作用是进行翻译 \n\n - 可以通过@机器人 **>{instrs_name}<翻译内容** 触发指令"
            message = {
                "msgtype": "markdown",
                "markdown": {
                    "text": f"#### {title}  \n\n{info}"
                }
            }
            return (message, None) , BotStatus.INSTRS_SET_SUCCESS
        
        message = {
            "msgtype": "text",
            "text": {
                "content": f"指令设置错误，请保持格式%instrs set 指令名称%"
            }
        }
        return (message, None) , BotStatus.INSTRS_SET_FAILED
    

class InstrsClsCommandStrategy(CommandStrategy):
    def __init__(self, robot, executor):
        self.executor = executor

    def execute(self, command_arg):
        if command_arg:
            # 清除指定指令的描述信息
            command_type = CommandType[command_arg.upper()]
            self.executor.set_instruction_desc(command_type, '')
            self.executor.set_instruction_example(command_type, '')
            return f"{command_type.name.lower()} 描述已清除"
        else:
            # 清除所有指令的描述信息
            for command_type in CommandType:
                self.executor.set_instruction_desc(command_type, '')
                self.executor.set_instruction_example(command_type, '')
            return "所有指令的描述已清除"
        