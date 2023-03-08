import unittest
from ..fixtures.test_data import BOT_DATA
from dbs.bots import bots

class TestDBBots(unittest.TestCase):
    def test_add_and_get_bot(self):
        # 添加一条记录
        bot = BOT_DATA[0]
        bots.add_bot(bot["robot_key"], bot["chat_id"], bot["hook"])

        # 根据robot_key获取记录
        record = bots.get_bot(bot["robot_key"])

        # 检查记录是否正确
        self.assertEqual(record["robot_key"], bot["robot_key"])
        self.assertEqual(record["chat_id"], bot["chat_id"])
        self.assertEqual(record["hook"], bot["hook"])

    # def test_get_by_robot_key(self):
    #     # 添加一条记录
    #     bots.add_bot("robot_key_2", "chat_id_2", "hook_2")

    #     # 获取记录
    #     record = bots.get_bot("robot_key_2")

    #     # 检查记录是否正确
    #     self.assertEqual(record["robot_key"], "robot_key_2")
    #     self.assertEqual(record["chat_id"], "chat_id_2")
    #     self.assertEqual(record["hook"], "hook_2")

    def test_get_by_nonexistent_robot_key(self):
        # 获取不存在的记录
        record = bots.get_bot("nonexistent_robot_key")

        # 检查记录是否为None
        self.assertEqual(record, None)

if __name__ == '__main__':
    unittest.main()
