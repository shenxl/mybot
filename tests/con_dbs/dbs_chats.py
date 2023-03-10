import unittest
from ..fixtures.mock_data import CHAT_DATA
from dbs.firedb import Chats

chats = Chats(collection_name=u"t_chats")
class TestDBChats(unittest.TestCase):
    def test_add_message(self):
        chat = CHAT_DATA[0]
        chats.add_message(user_id=chat["user_id"], role=chat["role"], 
                        robot_key=chat["robot_key"], content=chat["content"], parent_id=chat["parent_id"])
        # chats.add_message("userID_1", "assistant", "Hello")

        # 根据userID获取记录
        records = chats.get_by_userID(chat["user_id"])

        # 检查记录是否正确
        # self.assertEqual(len(record), 1)
        self.assertEqual(records[0]["user_id"], chat["user_id"])
        self.assertEqual(records[0]["role"], chat["role"])
        self.assertEqual(records[0]["content"], chat["content"])
        self.assertEqual(records[0]["robot_key"], chat["robot_key"])
        
        # 处理后清除所有记录
        chats.clear_by_userID(chat["user_id"])
    
    
    def test_get_by_nonexistent_userID(self):
        # 获取不存在的记录
        record = chats.get_by_userID("nonexistent_userID")

        # 检查记录是否为空列表
        self.assertEqual(len(record), 0)
        
    def test_get_by_userID(self):
        search_chat = CHAT_DATA[0]
        for chat in CHAT_DATA:
            chats.add_message(user_id=chat["user_id"], role=chat["role"], 
                robot_key=chat["robot_key"], content=chat["content"], parent_id=chat["parent_id"])
        db_records = chats.get_by_userID(search_chat["user_id"])
        
        
        source_result = [item for item in CHAT_DATA if item["user_id"] == search_chat["user_id"]]
        # source_result_str = str(source_result)
        # db_records_str = str(db_records)
        # # 使用 assertEqual 比较它们的字符串表示
        # self.assertEqual(source_result_str, db_records_str)
        
        # 每次获取的列表与原列表中的值相同
        self.assertEqual(len(db_records), len(source_result))
        
        user_ids = list({item["user_id"] for item in CHAT_DATA})
        for id in user_ids:
            chats.clear_by_userID(id)
    
    def test_get_by_userID_role(self):
        search_chat = CHAT_DATA[0]
        for chat in CHAT_DATA:
            chats.add_message(user_id=chat["user_id"], role=chat["role"], 
                robot_key=chat["robot_key"], content=chat["content"], parent_id=chat["parent_id"])
        db_records = chats.get_by_role(search_chat["user_id"], search_chat["role"])
        
        
        source_result = [item for item in CHAT_DATA if item["user_id"] == search_chat["user_id"] 
                            and item["role"] == search_chat["role"] ]
        # source_result_str = str(source_result)
        # db_records_str = str(db_records)
        # # 使用 assertEqual 比较它们的字符串表示
        # self.assertEqual(source_result_str, db_records_str)
        
        # 每次获取的列表与原列表中的值相同
        self.assertEqual(len(db_records), len(source_result))
        
        user_ids = list({item["user_id"] for item in CHAT_DATA})
        for id in user_ids:
            chats.clear_by_userID(id)
    
    def test_clear_chats(self):
            
        user_ids = list({item["user_id"] for item in CHAT_DATA})
        for id in user_ids:
            chats.clear_by_userID(id)
            record = chats.get_by_userID(id)
            self.assertEqual(len(record), 0)
                
        
        
        
        



if __name__ == '__main__':
    unittest.main()
