import unittest
from commands.executor import CommandExecutor
from commands.chats import ChatsClsCommandStrategy
from commands.init import InitCommandStrategy
from commands.instrs import InstrsCommandStrategy, InstrsSetCommandStrategy, InstrsClsCommandStrategy
from commands.executor import RekeyCommandStrategy
from commands.executor import HelpCommandStrategy
from commands.parse import CommandType
from commands.message import MessageCommandStrategy

class TestCommandExecutor(unittest.TestCase):
    def setUp(self):
        robot = {
            "userID": "user2",
            "robot_key": "robot1",
            "role": "assistant",
            "content": "content2",
            "parentid": None,
        }
        
        self.executor = CommandExecutor()
        # self.executor.add_strategy(CommandType.CHATS_CLS, ChatsClsCommandStrategy())
        self.executor.add_strategy(CommandType.INIT, InitCommandStrategy())
        # self.executor.add_strategy(CommandType.INSTRS, InstrsCommandStrategy())
        # self.executor.add_strategy(CommandType.INSTRS_SET, InstrsSetCommandStrategy())
        # self.executor.add_strategy(CommandType.INSTRS_CLS, InstrsClsCommandStrategy())
        self.executor.add_strategy(CommandType.REKEY, RekeyCommandStrategy())
        self.executor.add_strategy(CommandType.MSG, MessageCommandStrategy())
        # self.executor.add_strategy(CommandType.HELP, HelpCommandStrategy())

    # def test_chats_cls(self):
    #     result = self.executor.execute("@xxx %chat cls 10%")
    #     self.assertEqual(result, "已清理最近10条聊天记录。")

    # def test_chats_cls_default(self):
    #     result = self.executor.execute("@xxx %chat cls%")
    #     self.assertEqual(result, "已清理所有聊天记录。")

    # def test_chats_cls_invalid_args(self):
    #     with self.assertRaises(ValueError):
    #         self.executor.execute("@xxx %chat cls abc%")

    def test_init(self):
        robot = {
            "userID": "user2",
            "robot_key": "robot1",
            "role": "assistant",
            "content": "content2",
            "parentid": None,
        }
        
        result = self.executor.execute(robot, "@xxx %init%")
        self.assertEqual(result, "机器人user2已初始化完成")

    # def test_instrs(self):
    #     result = self.executor.execute("@xxx %instrs%")
    #     self.assertIn("instrs", result)
    #     self.assertIn("chats_cls", result)
    #     self.assertIn("init", result)

    # def test_instrs_set(self):
    #     result = self.executor.execute("@xxx %instrs set #chats_cls% 清空聊天记录")
    #     self.assertEqual(result, "指令 #chats_cls 已修改为“清空聊天记录”。")

    # def test_instrs_set_with_params(self):
    #     result = self.executor.execute("@xxx %instrs set #init code=12345% 初始化机器人")
    #     self.assertEqual(result, "指令 #init 已修改为“初始化机器人”。")

    # def test_instrs_set_with_invalid_args(self):
    #     with self.assertRaises(ValueError):
    #         self.executor.execute("@xxx %instrs set #chats_cls code=12345% 清空聊天记录")

    # def test_instrs_cls(self):
    #     result = self.executor.execute("@xxx %instrs cls #chats_cls%")
    #     self.assertEqual(result, "指令 #chats_cls 已清除。")

    # def test_instrs_cls_default(self):
    #     result = self.executor.execute("@xxx %instrs cls%")
    #     self.assertEqual(result, "所有指令已清除。")

    def test_rekey(self):
        robot = {
            "userID": "user2",
            "robot_key": "robot1",
            "role": "assistant",
            "content": "content2",
            "parentid": None,
        }
        
        result = self.executor.execute(robot, "@xxx %rekey%")
        self.assertEqual(result, "user2秘钥更换完成")

    # def test_help(self):
    #     result = self.executor.execute("@xxx %help%")
    #     self.assertIn("chats_cls", result)
    #     self.assertIn("init", result)
        
    def test_message(self):
        robot = {
            "userID": "user2",
            "robot_key": "robot1",
            "role": "assistant",
            "content": "content2",
            "parentid": None,
        }
        
        result = self.executor.execute(robot, "@xxx hello world")
        self.assertEqual(result, "user2say:hello world")

if __name__ == '__main__':
    unittest.main()
