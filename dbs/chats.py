# -*- coding: utf-8 -*-
from firebase_admin import firestore
from .firedb import Firebase

class Chats:
    def __init__(self,  db=None, collection_name=u"chats"):
        if db is None:
            self.db = Firebase.getInstance().db
        else:
            self.db = db
        self.collection_name = collection_name

    def add_message(self, user_id, role, content, robot_key, usage=None, parent_id=None):
        doc_ref = self.db.collection(self.collection_name).document()
        doc_ref.set({
            u"user_id": user_id,
            u"role": role,
            u"usage": usage,
            u"content": content,
            u"robot_key":robot_key,
            u"parent_id": parent_id if parent_id is not None else '',
            u"created": firestore.SERVER_TIMESTAMP,
        })
        return doc_ref.id

    def get_chats(self, robot_key, user_id=None, roles=[], channel=None):
        query = self.db.collection(self.collection_name)
        query = query.where(u"robot_key", "==", robot_key)
        if channel is not None:
            query = query.where(u"channel", "==", channel)
        if user_id is not None:
            query = query.where(u"user_id", "==", user_id)
        if len(roles) > 0:
            for role in roles:
                query = query.where(u"role", "==", role)

        query = query.order_by(u"created")
        
        docs = query.stream()
        return [doc.to_dict() for doc in docs]    
    
    def delete_by_id(self, record_id):
        doc_ref = self.db.collection(self.collection_name)
        doc_ref = doc_ref.document(record_id)
        doc_ref.delete()      
    
    
    def clear_by_robot(self, robot_key, channel=None, user_id=None, roles=[]):
        query = self.db.collection(self.collection_name)
        query = query.where(u"robot_key", "==", robot_key)
        if channel is not None:
            query = query.where(u"channel", "==", channel)
        if user_id is not None:
            query = query.where(u"user_id", "==", user_id)
        if len(roles) > 0:
            for role in roles:
                query = query.where(u"role", "==", role)
        docs = query.stream()
        for doc in docs:
            doc.reference.delete()
