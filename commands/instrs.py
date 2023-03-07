from .executor import CommandStrategy, CommandType

# TODO： 思考指令相关的逻辑
class InstrsCommandStrategy(CommandStrategy):
    def __init__(self, executor):
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

    def execute(self, command_arg):
        parts = command_arg.split(maxsplit=1)
        command_type_str = parts[0].upper()
        if len(parts) > 1:
            desc = parts[1]
            if desc:
                if command_type_str.startswith("#") and len(command_type_str) > 1:
                    # 自动为指令命名
                    name = command_type_str[1:] if len(command_type_str) <= 9 else command_type_str[1:9]
                    command_type = CommandType[f"{name.upper()}_SET"]
                else:
                    command_type = CommandType[f"{command_type_str}_SET"]
                self.executor.set_instruction_desc(command_type, desc)
                return f"{command_type.name.lower()} 描述已更新"
        return f"指令 {command_type_str.lower()} 不存在"
    

class InstrsClsCommandStrategy(CommandStrategy):
    def __init__(self, executor):
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
        