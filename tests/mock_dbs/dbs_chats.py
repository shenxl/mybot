# tests/test_chats.py

import unittest
from unittest import mock
from fixtures.firebase_mock import create_mock_firestore, MockFirebase
from fixtures.test_data import CHAT_DATA
from dbs.firedb import Chats

class TestDBChats(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app_mock, cls.db_mock = create_mock_firestore()
        cls.chats = Chats(cls.db_mock)
        # 向数据库中插入测试数据

    def test_add_message(self):
        # 测试 add_message() 函数
        for chat in CHAT_DATA:
            result = self.chats.add_message(chat["userID"], chat["role"], chat["content"], chat["parentid"])
            self.assertIsNotNone(result)
            
        for chat in CHAT_DATA:
            self.db_mock.set.assert_any_call({
                "userID": chat["userID"],
                "role": chat["role"],
                "created": mock.ANY,
                "content": chat["content"],
                "parentid": chat["parentid"] or "",
            })

    def test_get_by_userID(self):
        for chat in CHAT_DATA:
            result = self.chats.add_message(chat["userID"], chat["role"], chat["content"], chat["parentid"])
            self.assertIsNotNone(result)
        # expected_len = len(CHAT_DATA)
        # mock_len = len(self.db_mock.where.return_value.stream.return_value)
        # self.assertEqual(mock_len, expected_len)
        
        query = self.db_mock.collection.return_value.where
        self.assertEqual(query.call_args_list[0], mock.call("userID", "==", "user1"))
        
        result = self.chats.get_by_userID("user1")
        self.assertEqual(len(result), 2)
        

        
    def test_delete_by_id(self):
        # 测试 delete_by_id() 函数
        chat = CHAT_DATA[0]
        record_id = self.chats.add_message(chat["userID"], chat["role"], chat["content"], chat["parentid"])
        self.assertIsNotNone(record_id)
        result = self.chats.get_by_userID("user1")
        self.assertEqual(len(result), 3)
        self.chats.delete_by_id(record_id)
        result = self.chats.get_by_userID("user1")
        self.assertEqual(len(result), 2)

    def test_clear_by_userID(self):
        # 测试 clear_by_userID() 函数
        self.chats.clear_by_userID("user1")
        result = self.chats.get_by_userID("user1")
        self.assertEqual(len(result), 0)
        
    @classmethod
    def tearDownClass(cls):
        MockFirebase.cleanup()

    def tearDown(self):
        self.db_mock.reset_mock()   # 清空数据库状态
