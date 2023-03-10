from enum import Enum


class BotStatus(Enum):
    Exception = 0
    UNREGISTERED = 1
    PROCESSING = 2
    REGISTERED = 3
    REGISTRATION_FAILED = 4
    REPLY = 5
    REPLY_ERROR =6
    CLEAR_ALL_CHATS = 7
    HOOKKEY_NONE = 8
    HELP_LIST = 9
    COMPRESSED = 10
    COMPRESSION_FAILED = 11