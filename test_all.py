# -*- coding: utf-8 -*-
import unittest
import sys
print(sys.path)
# 加载所有测试用例
# from mock_dbs.dbs_bots import TestDBBots
# from mock_dbs.dbs_sks import TestDBSKs
# from mock_dbs.dbs_chats import TestDBChats
from tests.tests_mock_commands.tests_parse import TestParseCommands
from tests.tests_mock_commands.tests_exec import TestCommandExecutor
# from test_app_chat import TestAppChat

# from dbs.bots import bots

if __name__ == '__main__':

    # 创建测试套件
    suite = unittest.TestSuite()
    # 添加所有测试用例到测试套件
    # 数据库的测试用例，不需要每次都跑
    # suite.addTest(unittest.makeSuite(TestDBBots))
    # suite.addTest(unittest.makeSuite(TestDBSKs))
    # suite.addTest(unittest.makeSuite(TestDBChats))
    suite.addTest(unittest.makeSuite(TestParseCommands))
    suite.addTest(unittest.makeSuite(TestCommandExecutor))
    # suite.addTest(unittest.makeSuite(TestAppChat))
    # 创建测试运行器并运行测试套件
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
