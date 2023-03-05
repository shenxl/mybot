import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dbs.bots import bots

class TestDBBots(unittest.TestCase):
    def test_add_bot(self):
        # 添加一条记录
        bots.add_bot("robot_key_1", "chat_id_1", "hook_1")

        # 根据robot_key获取记录
        record = bots.get_bot("robot_key_1")

        # 检查记录是否正确
        self.assertEqual(record["robot_key"], "robot_key_1")
        self.assertEqual(record["chat_id"], "chat_id_1")
        self.assertEqual(record["hook"], "hook_1")

    def test_get_by_robot_key(self):
        # 添加一条记录
        bots.add_bot("robot_key_2", "chat_id_2", "hook_2")

        # 获取记录
        record = bots.get_bot("robot_key_2")

        # 检查记录是否正确
        self.assertEqual(record["robot_key"], "robot_key_2")
        self.assertEqual(record["chat_id"], "chat_id_2")
        self.assertEqual(record["hook"], "hook_2")

    def test_get_by_nonexistent_robot_key(self):
        # 获取不存在的记录
        record = bots.get_bot("nonexistent_robot_key")

        # 检查记录是否为None
        self.assertEqual(record, None)

if __name__ == '__main__':
    unittest.main()
