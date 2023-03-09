import unittest
from ..fixtures.mock_data import BOT_DATA
from dbs.firedb import Bots


bots = Bots(collection_name=u"t_bots")
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

    def test_get_by_robot_key(self):
        # 添加一条记录
        for bot in BOT_DATA:
            bots.add_bot(bot["robot_key"], bot["chat_id"], bot["hook"])
        
        get_bot = BOT_DATA[-1]
        
        record = bots.get_bot(get_bot["robot_key"])

        # 检查记录是否正确
        self.assertEqual(record["robot_key"], get_bot["robot_key"])
        self.assertEqual(record["chat_id"], get_bot["chat_id"])
        self.assertEqual(record["hook"], get_bot["hook"])

    def test_get_by_nonexistent_robot_key(self):
        # 获取不存在的记录
        record = bots.get_bot("nonexistent_robot_key")

        # 检查记录是否为None
        self.assertEqual(record, None)

if __name__ == '__main__':
    unittest.main()
