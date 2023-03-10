# -*- coding: utf-8 -*-
from firebase_admin import firestore
from .firedb import Firebase


"""_summary_
指令的生成规则：

1. 看命令是否与 ACT 有关,如果有关, 是一次性对话, 无需处理上下文。

2. 若无关，先看内置指令是否存: 即get_systems_prompt create_tag="inter" & catagory="system",内置存在则附加到 prompt 的起始位置
3. 看压缩指令是否存在，压缩指令与 robot_key \ channel 相关。
4. 若是 ACT 则为一次性对话, 不引入上下文(也不会存储)
5. 若是 对话 则再处理上下文, 从chats中获取相应规则的对话,与 robot_key \ channel 相关。

6. get_act_prompts 提供给帮助指令，展示当前存在的角色，分内置与自定义。
Returns:
    _type_: _description_
"""
class Prompts:

    def __init__(self,  db=None, collection_name=u"prompts"):
        if db is None:
            self.db = Firebase.getInstance().db
        else:
            self.db = db
        self.collection_name = collection_name
    """
    create_tag : 分为 内置 (inter) \ 自定义 (user_id) \ 压缩 (summary)
    catagory : 分为 指令 (system) \  角色扮演 (act)
    des: 只针对角色有效
    """
    
    def add_prompt(self, create_tag, robot_key, promot, 
                catagory="system",des=None , channel=None):
        doc_ref = self.db.collection(self.collection_name).document()
        doc_ref.set({
            u"create_tag": create_tag,
            u"robot_key": robot_key,
            u"promot": promot,
            u"catagory": catagory,
            u"robot_key":robot_key,
            u"des": des,
            u"channel": channel,
            u"created": firestore.SERVER_TIMESTAMP,
        })
        return doc_ref.id

    def get_prompts(self, robot_key=None, create_tag=None,
                catagory="system", des=None , channel=None):
        query = self.db.collection(self.collection_name)
        query = query.where(u"catagory", "==", catagory)
        if robot_key is not None:
            query = query.where(u"robot_key", "==", robot_key)
        if create_tag is not None:
            query = query.where(u"create_tag", "==", create_tag)
        if des is not None:
            query = query.where(u"des", "==", des)
        if channel is not None:
            query = query.where(u"channel", "==", channel)
            
        query = query.order_by(u"created")
        
        docs = query.stream()
        return [doc.to_dict() for doc in docs]
    
    # def get_prompts_by_user_or_bot(self, robot_key, create_tag,
    #             catagory="system", des=None , channel=None):
    #     query = self.db.collection(self.collection_name).where(u"catagory", "==", catagory)
    #     query_user = self.db.collection(self.collection_name).where(u"catagory", "==", catagory)
        
    #     query = query.where(u"robot_key", "==", robot_key)
    #     query_user = query_user.where(u"create_tag", "==", create_tag)
    #     query = query | query_user
    #     query = query.order_by(u"created")
        
    #     docs = query.stream()
    #     return [doc.to_dict() for doc in docs]

    # 获取内置 system 指令
    def get_systems_prompt(self):
        return self.get_prompts(create_tag="inter")

    # 获取当前用户的act system 指令
    def get_act_prompts(self, user_id):
        return self.get_prompts(create_tag=user_id, catagory="act")

    # 获取当前聊天下的act列表
    def get_act_prompt(self, des, user_id="inter"):
        return self.get_prompts(create_tag=user_id, des=des, catagory="act")


    # 获取压缩 system 指令, 压缩指令与 robot_key \ channel 相关。
    def get_summary_prompt(self, robot_key, channel=None):
        return self.get_prompts(create_tag="summary", robot_key=robot_key , channel=channel)