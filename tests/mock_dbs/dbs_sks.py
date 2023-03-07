# -*- coding: utf-8 -*-
import unittest
from fixtures.firebase_mock import create_mock_firestore, MockFirebase
from fixtures.test_data import SK_DATA
from dbs.firedb import SKs

class TestDBSKs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app_mock, cls.db_mock = create_mock_firestore()
        cls.sks = SKs(cls.db_mock)

    def test_add_sk(self):
        # 测试 add_sk() 函数
        for sk in SK_DATA:
            self.sks.add_sk(sk)
        for sk in SK_DATA:
            self.db_mock.set.assert_any_call({
                "sk": sk,
                "used": False,
            })

    def test_get_by_sk(self):
        # 测试 get_by_sk() 函数
        for sk in SK_DATA:
            self.db_mock.get.return_value.exists = True
            self.db_mock.get.return_value.to_dict.return_value = {
                "sk": sk,
                "used": False,
            }
            result = self.sks.get_by_sk(sk)
            self.assertEqual(result, {
                "sk": sk,
                "used": False,
            })

        # 测试不存在的情况
        self.db_mock.get.return_value.exists = False
        result = self.sks.get_by_sk("not_exist")
        self.assertIsNone(result)

    @classmethod
    def tearDownClass(cls):
        MockFirebase.cleanup()

    def tearDown(self):
        self.db_mock.reset_mock()   # 清空数据库状态