# -*- coding: utf-8 -*-
import socks
import socket
import os
import firebase_admin

from firebase_admin import credentials, firestore
from datetime import datetime
from logs.logger import Logger
from conf.config import  get_config


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
            Firebase.__instance = self
            cred = credentials.Certificate(get_config().FIREBASE_KEY)
            firebase_admin.initialize_app(cred, {
                'databaseURL': get_config().FIREBASE_DB_URL
            })
            Firebase.__instance = self
            self.db = firestore.client()



class Bots:
    def __init__(self, db=None, collection_name=u"bots"):
        if db is None:
            self.db = Firebase.getInstance().db
        else:
            self.db = db
        self.collection_name = collection_name

    def add_bot(self, robot_key, chat_id, hook):
        doc_ref = self.db.collection(self.collection_name)
        doc_ref = doc_ref.document(robot_key)
        
        doc_ref.set({
            u"robot_key": robot_key,
            u"chat_id": chat_id,
            u"hook": hook,
            u"created": firestore.SERVER_TIMESTAMP
        })
        
    def get_bot(self, robot_key):
        doc_ref = self.db.collection(self.collection_name)
        doc_ref = doc_ref.document(robot_key)
        
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None

class SKs:
    def __init__(self, db=None, collection_name=u"sks"):
        
        if db is None:
            self.db = Firebase.getInstance().db
        else:
            self.db = db
        self.collection_name = collection_name

    def add_sk(self, sk):
        doc_ref = self.db.collection(self.collection_name)
        doc_ref = doc_ref.document(sk)
        doc_ref.set({
            u"sk": sk,
            u"used": False
        })
        
    def get_by_sk(self, sk):
        doc_ref = self.db.collection(self.collection_name)
        doc_ref = doc_ref.document(sk)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None

class Chats:
    def __init__(self,  db=None, collection_name=u"chats"):
        if db is None:
            self.db = Firebase.getInstance().db
        else:
            self.db = db
        self.collection_name = collection_name

    def add_message(self, userID, role, content,robot_key, parentid=None):
        doc_ref = self.db.collection(self.collection_name).document()
        doc_ref.set({
            u"userID": userID,
            u"role": role,
            u"content": content,
            u"robot_key":robot_key,
            u"parentid": parentid if parentid is not None else '',
            u"created": firestore.SERVER_TIMESTAMP,
        })
        return doc_ref.id

    def delete_by_id(self, record_id):
        doc_ref = self.db.collection(self.collection_name)
        doc_ref = doc_ref.document(record_id)
        
        doc_ref.delete()
        
    def get_by_userID(self, userID):
        query = self.db.collection(self.collection_name)
        query = query.where(u"userID", "==", userID)
        query = query.order_by(u"created")
        
        docs = query.stream()
        return [doc.to_dict() for doc in docs]
    
    def get_by_role(self, userID, role):
        query = self.db.collection(self.collection_name)
        query = query.where(u"userID", "==", userID)
        query = query.where(u"role", "==", role)
        query = query.order_by(u"created")
        
        docs = query.stream()
        return [doc.to_dict() for doc in docs]
    
    def clear_by_userID(self, userID):
        query = self.db.collection(self.collection_name)
        query = query.where(u"userID", "==", userID)
        
        docs = query.stream()
        for doc in docs:
            doc.reference.delete()
