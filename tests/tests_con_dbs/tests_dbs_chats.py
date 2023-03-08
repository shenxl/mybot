import unittest
from dbs.chats import chats

class TestDBChats(unittest.TestCase):
    def test_add_message(self):
        chats.add_message("userID_1", "assistant", "Hello")

        # 根据userID获取记录
        record = chats.get_by_userID("userID_1")

        # 检查记录是否正确
        # self.assertEqual(len(record), 1)
        self.assertEqual(record[0]["userID"], "userID_1")
        self.assertEqual(record[0]["role"], "assistant")
        self.assertEqual(record[0]["content"], "Hello")

    def test_get_by_nonexistent_userID(self):
        # 获取不存在的记录
        record = chats.get_by_userID("nonexistent_userID")

        # 检查记录是否为空列表
        self.assertEqual(len(record), 0)

if __name__ == '__main__':
    unittest.main()
