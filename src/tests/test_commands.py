# -*- coding: utf-8 -*-
import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from commands.commands import CommandType ,parse_command

class TestCommands(unittest.TestCase):
    def test_parse_command(self):
        # 测试消息类型的输入字符串
        # 检查记录是否正确
        self.assertEqual(parse_command("@12313 bar"),(CommandType.MSG, "bar"))


        # 测试不合法的输入字符串datetime
        try:
            parse_command("foo bar")
        except ValueError:
            pass
        else:
            assert False, "没有抛出异常"

        # 测试 help 指令
        self.assertEqual(parse_command("@aaab %help %"), (CommandType.HELP, None))
        # 测试 init 指令
        self.assertEqual(parse_command("@cccd %init%"),(CommandType.INIT, None))
        # 测试 chats 指令
        self.assertEqual(parse_command("@foo %chats %") ,(CommandType.CHATS, None))

        # 测试 chats 指令
        self.assertEqual(parse_command("@foo %chats cls%") ,(CommandType.CHATS_CLS, None))
        
        # 测试 chat cls n 指令
        self.assertEqual(parse_command("@foo %chats cls  n%") , (CommandType.CHATS_CLS, "n"))

        # 测试 instrs 指令
        self.assertEqual(parse_command("@foo % instrs%") , (CommandType.INSTRS, None))

        # 测试 instrs set #xxx 指令
        self.assertEqual(parse_command("@foo %instrs set #name% ") , (CommandType.INSTRS_SET, "#name"))

        # 测试 instrs set指令
        self.assertEqual(parse_command("@foo %instrs set% ") , (CommandType.INSTRS_SET,None))

        # 测试 instrs cls #xxx 指令
        self.assertEqual(parse_command("@foo %instrs cls %") , (CommandType.INSTRS_CLS, None))
        
        # 测试 instrs cls #xxx 指令
        self.assertEqual(parse_command("@foo %instrs cls  #xxx%") , (CommandType.INSTRS_CLS, "#xxx"))

        # 测试 instrs cls #xxx 指令
        self.assertEqual(parse_command("@foo %1instrs cls  #xxx%") , (CommandType.UNKNOWN, "#xxx"))

        # 测试 rekey 指令
        self.assertEqual(parse_command("@foo %rekey%") , (CommandType.REKEY, None))
    
    
if __name__ == "__main__":
    unittest.main()