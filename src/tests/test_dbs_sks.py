# -*- coding: utf-8 -*-
import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dbs.sks import sks

class TestDBSKs(unittest.TestCase):
    def test_add_sk(self):
        # 添加一条记录
        sks.add_sk("sk_1")

        # 根据sk获取记录
        record = sks.get_by_sk("sk_1")

        # 检查记录是否正确
        self.assertEqual(record["sk"], "sk_1")
        self.assertEqual(record["used"], False)

    def test_get_by_nonexistent_sk(self):
        # 获取不存在的记录
        record = sks.get_by_sk("nonexistent_sk")

        # 检查记录是否为None
        self.assertEqual(record, None)

if __name__ == '__main__':
    unittest.main()
