import socks
import socket
import os
import firebase_admin

from firebase_admin import credentials, firestore
from datetime import datetime
from src.logs.logger import Logger
from src.conf.config import  get_config


# 设置日志
logger = Logger(__name__)
env = os.environ.get('ENV')
if env != 'prod':
    logger.info("非生产环境，启动代理")
    # 设置代理
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:8889'
    # 设置 Socks 代理 访问 firebase (调试中需要)
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", port=1089)
    socket.socket = socks.socksocket


class Firebase:
    __instance = None

    @staticmethod
    def getInstance():
        if Firebase.__instance == None:
            Firebase()
        return Firebase.__instance
    
    def __init__(self):
        if Firebase.__instance is not None:
            raise Exception("Firebase class is a singleton!")
        else:
            cred = credentials.Certificate(get_config().FIREBASE_KEY)
            firebase_admin.initialize_app(cred, {
                'databaseURL': get_config().FIREBASE_DB_URL
            })
            Firebase.__instance = self
            self.db = firestore.client()


class Bots:
    def __init__(self):
        self.collection_name = "bots"
        self.db = Firebase.getInstance().db

    def add_bot(self, robot_key, chat_id, hook):
        doc_ref = self.db.collection(self.collection_name).document(robot_key)
        doc_ref.set({
            "robot_key": robot_key,
            "chat_id": chat_id,
            "hook": hook,
            "created": firestore.SERVER_TIMESTAMP
        })
        
    def get_bot(self, robot_key):
        doc_ref = self.db.collection(self.collection_name).document(robot_key)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None

class SKs:
    def __init__(self):
        self.collection_name = "sks"
        self.db = Firebase.getInstance().db

    def add_sk(self, sk):
        doc_ref = self.db.collection(self.collection_name).document(sk)
        doc_ref.set({
            "sk": sk,
            "used": False
        })
    def get_by_sk(self, sk):
        doc_ref = self.db.collection(self.collection_name).document(sk)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None

class Chats:
    def __init__(self):
        self.collection_name = "chats"
        self.db = Firebase.getInstance().db

    def add_message(self, userID, role, content, parentid=None):
        doc_ref = self.db.collection(self.collection_name).document()
        doc_ref.set({
            "userID": userID,
            "role": role,
            "created": firestore.SERVER_TIMESTAMP,
            "content": content,
            "parentid": parentid if parentid is not None else '',
        })
        return doc_ref.id

    def delete_by_id(self, record_id):
        doc_ref = self.db.collection(self.collection_name).document(record_id)
        doc_ref.delete()
        
    def get_by_userID(self, userID):
        query = self.db.collection(self.collection_name).where("userID", "==", userID).order_by("created")
        docs = query.stream()
        return [doc.to_dict() for doc in docs]
    
    def clear_by_userID(self, userID):
        query = self.db.collection(self.collection_name).where('userID', '==', userID)
        docs = query.stream()
        for doc in docs:
            doc.reference.delete()
