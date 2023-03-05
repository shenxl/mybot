import unittest

# 加载所有测试用例
from test_dbs_bots import TestDBBots
from test_dbs_sks import TestDBSKs
from test_dbs_chats import TestDBChats
from test_commands import TestCommands
from test_app_chat import TestAppChat

# from dbs.bots import bots

if __name__ == '__main__':
    # 创建测试套件
    suite = unittest.TestSuite()

    # 添加所有测试用例到测试套件
    # 数据库的测试用例，不需要每次都跑
    # suite.addTest(unittest.makeSuite(TestDBBots))
    # suite.addTest(unittest.makeSuite(TestDBSKs))
    # suite.addTest(unittest.makeSuite(TestDBChats))
    suite.addTest(unittest.makeSuite(TestCommands))
    suite.addTest(unittest.makeSuite(TestAppChat))
    # 创建测试运行器并运行测试套件
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
