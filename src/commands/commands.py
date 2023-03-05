# -*- coding: utf-8 -*-
from enum import Enum

class CommandType(Enum):
    HELP = 1
    INIT = 2
    CHATS = 3
    CHATS_CLS = 4
    INSTRS = 5
    INSTRS_SET = 6
    INSTRS_CLS = 7
    REKEY = 8
    UNKNOWN = 10
    MSG = 0


def parse_command(input_str):
    """
    根据输入字符串，解析出指令或消息类型，并返回相应的信息

    Args:
        input_str: str, 输入字符串，格式为 "@xxx str"，其中 xxx 为任意字符，str 中间有空格

    Returns:
        如果输入字符串为指令类型，则返回一个元组 (command_type, command_arg)，其中：
            - command_type: CommandType 枚举值，表示指令类型
            - command_arg: str，表示指令参数
        如果输入字符串为消息类型，则返回一个元组 (None, message)，其中：
            - message: str，表示消息内容
    """
    # 判断输入字符串是否为空或格式是否正确
    if not input_str.startswith("@"):
        raise ValueError("输入字符串格式错误")

    # 解析出指令或消息类型
    command_str, message = input_str[1:].split(" ", 1)
    if message.startswith("%"):
        # 指令类型
        command_type, command_arg = parse_instruction(message)
        return command_type, command_arg
    else:
        # 消息类型
        return CommandType.MSG, message

def parse_instruction(instruction_str):
    """
    根据指令字符串，解析出指令类型和参数，并返回相应的信息

    Args:
        instruction_str: str, 指令字符串，格式为 "%xxx% arg"，其中 xxx 为任意字符，arg 可选

    Returns:
        一个元组 (command_type, command_arg)，其中：
            - command_type: CommandType 枚举值，表示指令类型
            - command_arg: str，表示指令参数，如果没有参数则为 None
    """
    # 判断输入字符串是否为空或格式是否正确
    instruction_str = instruction_str.strip()
    if not instruction_str.startswith("%") or not instruction_str.endswith("%"):
        raise ValueError("指令字符串格式错误")

    # 分割指令字符串
 
    parts = instruction_str[1:-1].strip().split()
    command_type_str = parts[0].upper()
        # 根据分割后的部分确定指令类型和参数
    if len(parts) == 3:
        command_type_str = f"{command_type_str}_{parts[1].upper()}"
        try:
            command_type = CommandType[command_type_str]
        except KeyError:
            command_type = CommandType.UNKNOWN
        command_arg = parts[2] if len(parts) > 2 else None
    elif len(parts) == 2:
        command_type_str = f"{command_type_str}_{parts[1].upper()}"
        try:
            command_type = CommandType[command_type_str]
        except KeyError:
            command_type = CommandType.UNKNOWN
        command_arg = None
    else:
        # 其他指令
        try:
            command_type = CommandType[command_type_str]
        except KeyError:
            command_type = CommandType.UNKNOWN
        command_arg = parts[1] if len(parts) > 1 else None
    return command_type, command_arg
