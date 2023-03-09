# tests/test_data.py

BOT_DATA = [
    {
        "robot_key": "shenxl1",
        "chat_id": "haha",
        "hook": "hook1",
    },
    {
        "robot_key": "shenxr",
        "chat_id": "hehe",
        "hook": "hook2",
    },
]

CHAT_DATA = [
    {
        "userID": "user1",
        "robot_key": "robot1",
        "role": "user",
        "content": "content1",
        "parentid": None,
    },
    {
        "userID": "user1",
        "robot_key": "robot1",
        "role": "assistant",
        "content": "content2",
        "parentid": None,
    },
    {
        "userID": "user1",
        "robot_key": "robot1",
        "role": "user",
        "content": "content1-111",
        "parentid": None,
    },
    {
        "userID": "user1",
        "robot_key": "robot1",
        "role": "assistant",
        "content": "content2-111",
        "parentid": None,
    },    
    {
        "userID": "user2",
        "robot_key": "robot1",
        "role": "user",
        "content": "content1",
        "parentid": None,
    },
    {
        "userID": "user2",
        "robot_key": "robot1",
        "role": "assistant",
        "content": "content2",
        "parentid": None,
    },
    {
        "userID": "user1",
        "robot_key": "robot1",
        "role": "system",
        "content": "content2",
        "parentid":  None,
    },
    {
        "userID": "internel",
        "robot_key": "robot1",
        "role": "system",
        "content": "xxxxxxx",
        "parentid":  None,
    },
]

SK_DATA = [
    "sk1",
    "sk2",
]
