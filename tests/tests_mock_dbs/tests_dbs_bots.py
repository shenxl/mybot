# tests/test_bots.py

import unittest
from unittest import mock   # 添加这一行导入语句
from fixtures.firebase_mock import create_mock_firestore, MockFirebase
from fixtures.test_data import BOT_DATA
from dbs.firedb import Bots


class TestDBBots(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app_mock, cls.db_mock = create_mock_firestore()
        cls.bots = Bots(cls.db_mock)

    def test_add_bot(self):
        # 测试 add_bot() 函数
        for bot in BOT_DATA:
            self.bots.add_bot(bot["robot_key"], bot["chat_id"], bot["hook"])
        for bot in BOT_DATA:
            self.db_mock.set.assert_any_call({
                "robot_key": bot["robot_key"],
                "chat_id": bot["chat_id"],
                "hook": bot["hook"],
                "created": mock.ANY,
            })
        mock_len = len(self.db_mock.where.return_value.stream.return_value)
        print("after add", mock_len)

    def test_get_bot(self):
        # 测试 get_bot() 函数
        for bot in BOT_DATA:
            self.db_mock.get.return_value.exists = True
            self.db_mock.get.return_value.to_dict.return_value = {
                "robot_key": bot["robot_key"],
                "chat_id": bot["chat_id"],
                "hook": bot["hook"],
                "created": mock.ANY,
            }
            result = self.bots.get_bot(bot["robot_key"])
            self.assertEqual(result, {
                "robot_key": bot["robot_key"],
                "chat_id": bot["chat_id"],
                "hook": bot["hook"],
                "created": mock.ANY,
            })


    @classmethod
    def tearDownClass(cls):
        MockFirebase.cleanup()
