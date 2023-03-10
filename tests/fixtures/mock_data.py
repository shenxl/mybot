# tests/test_data.py

BOT_DATA = [
    {
        "robot_key": "shenxl1",
        "user_id": "haha",
        "hook": "hook1",
    },
    {
        "robot_key": "shenxr",
        "user_id": "hehe",
        "hook": "hook2",
    },
]

CHAT_DATA = [
    {
        "user_id": "user1",
        "robot_key": "robot1",
        "role": "user",
        "content": "content1",
        "parent_id": None,
    },
    {
        "user_id": "user1",
        "robot_key": "robot1",
        "role": "assistant",
        "content": "content2",
        "parent_id": None,
    },
    {
        "user_id": "user1",
        "robot_key": "robot1",
        "role": "user",
        "content": "content1-111",
        "parent_id": None,
    },
    {
        "user_id": "user1",
        "robot_key": "robot1",
        "role": "assistant",
        "content": "content2-111",
        "parent_id": None,
    },    
    {
        "user_id": "user2",
        "robot_key": "robot1",
        "role": "user",
        "content": "content1",
        "parent_id": None,
    },
    {
        "user_id": "user2",
        "robot_key": "robot1",
        "role": "assistant",
        "content": "content2",
        "parent_id": None,
    },
    {
        "user_id": "user1",
        "robot_key": "robot1",
        "role": "system",
        "content": "content2",
        "parent_id":  None,
    },
    {
        "user_id": "internel",
        "robot_key": "robot1",
        "role": "system",
        "content": "xxxxxxx",
        "parent_id":  None,
    },
]

SK_DATA = [
    "sk1",
    "sk2",
]
