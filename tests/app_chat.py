# -*- coding: utf-8 -*-
import json
import unittest
from unittest.mock import patch
from server import app

class TestAppChat(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_get_chat(self):
        response = self.client.get("/chat")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"result": "ok"})

    def test_post_chat_with_unregistered_bot(self):
        data = {
            "chatid": 2902558,
            "creator": 1385942343,
            "content": "@自定义机器人 %help%",
            "robot_key": "d57a91bf7c8cdb2213ed493f6a3127d1",
            "url": "https://f1bc8b53-fb53-4370-83d1-85dfaf6c8e00.mock.pstmn.io/mock",
            "ctime": 1677849373
        }
        response = self.client.post("/chat", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"message": "机器人未注册"})

    def test_post_chat_with_invalid_url(self):
        data = {
            "chatid": 2902558,
            "creator": 1385942343,
            "content": "@xxx %init%",
            "robot_key": "valid_key",
            "url": "https://f1bc8b53-fb53-4370-83d1-85dfaf6c8e00.mock.pstmn.io/mock",
            "ctime": 1677849373
        }
        response = self.client.post("/chat", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"message": "注册失败"})

    def test_post_chat_with_valid_data(self):
        data = {
            "chatid": 2902558,
            "creator": 1385942343,
            "content": "@xxx %init%",
            "robot_key": "valid_key",
            "url": "https://f1bc8b53-fb53-4370-83d1-85dfaf6c8e00.mock.pstmn.io/mock?key=valid_key",
            "ctime": 1677849373
        }
        response = self.client.post("/chat", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"message": "注册成功"})

    def test_post_chat_with_invalid_content(self):
        data = {
            "chatid": 2902558,
            "creator": 1385942343,
            "content": "@xxx invalid content",
            "robot_key": "shenxl",
            "url": "https://f1bc8b53-fb53-4370-83d1-85dfaf6c8e00.mock.pstmn.io/mock?key=valid_key",
            "ctime": 1677849373
        }
        response = self.client.post("/chat", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"message": "正常消息处理"})
