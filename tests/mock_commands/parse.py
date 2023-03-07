import unittest

from commands.parse import parse_command, CommandType


class TestParseCommands(unittest.TestCase):

    def test_parse_command_help(self):
        result = parse_command("@user %help%")
        self.assertEqual(result, (CommandType.HELP, None))
    
    # @不在指令的最前端的情况
    def test_parse_command_help_at(self):
        result = parse_command(" %help% @沈霄雷 ") 
        self.assertEqual(result, (CommandType.HELP, None))

    def test_parse_command_init(self):
        result = parse_command("@user %init%" )
        self.assertEqual(result, (CommandType.INIT, None))
    
    def test_parse_command_init_unknow(self):
        result = parse_command("@user %init% unknow" )
        self.assertEqual(result, (CommandType.UNKNOWN, None))
    
    # 指令中包括多种空格的情况
    def test_parse_command_init_at_space(self):
        result = parse_command("@user  %init % ")
        self.assertEqual(result, (CommandType.INIT, None))
    
    def test_parse_command_init_space(self):
        result = parse_command("@user %init%  sdsaa")
        self.assertEqual(result, (CommandType.UNKNOWN, None))

    def test_parse_command_chats(self):
        result = parse_command("@user %chats%")
        self.assertEqual(result, (CommandType.CHATS, None))

    def test_parse_command_chats_cls_all(self):
        result = parse_command("@user %chats cls%")
        self.assertEqual(result, (CommandType.CHATS_CLS, None))

    def test_parse_command_chats_cls_n(self):
        result = parse_command("@user %chats cls 5%")
        self.assertEqual(result, (CommandType.CHATS_CLS, "5"))

    def test_parse_command_instrs(self):
        result = parse_command("@user %instrs%")
        self.assertEqual(result, (CommandType.INSTRS, None))

    def test_parse_command_instrs_set(self):
        result = parse_command("@user %instrs set #xxx%")
        self.assertEqual(result, (CommandType.INSTRS_SET, "#xxx"))
        
    def test_parse_command_instrs_set_des(self):
        result = parse_command("@user %instrs set #xxx 哈哈哈哈哈%")
        self.assertEqual(result, (CommandType.INSTRS_SET, "#xxx 哈哈哈哈哈"))

    def test_parse_command_instrs_cls_all(self):
        result = parse_command("@user %instrs cls%")
        self.assertEqual(result, (CommandType.INSTRS_CLS, None))

    def test_parse_command_instrs_cls(self):
        result = parse_command("@user %instrs cls #xxx%")
        self.assertEqual(result, (CommandType.INSTRS_CLS, "#xxx"))

    def test_parse_command_rekey(self):
        result = parse_command("@user %rekey%")
        self.assertEqual(result, (CommandType.REKEY, None))

    def test_parse_command_topic(self):
        result = parse_command("@user %topic%")
        self.assertEqual(result, (CommandType.UNKNOWN, None))

    def test_parse_command_message(self):
        result = parse_command("@user hello")
        self.assertEqual(result, (CommandType.MSG, "hello"))

    # @不是在第一处的情况
    def test_parse_command_message_at(self):
        result = parse_command("123456@沈霄雷 7890")
        self.assertEqual(result, (CommandType.MSG, "1234567890"))

    def test_parse_command_unknown_command(self):
        result = parse_command("@user %invalid%")
        self.assertEqual(result, (CommandType.UNKNOWN, None))

if __name__ == '__main__':
    unittest.main()
