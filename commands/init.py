from .executor import CommandStrategy
from dbs.bots import bots
from logs.logger import Logger
from app.botstatus import BotStatus
from conf.config import get_config
# 设置日志
logger = Logger(__name__)
# bots = Bots(collection_name=u't_bots')
class InitCommandStrategy(CommandStrategy):
    def execute(self, robot, command_arg):
        bot_info = bots.get_bot(robot[u"robot_key"])
        if bot_info is None and "hook_key" in robot:
            # 将 url 和 key 拼接成完整的 hook_url，并注册机器人
            hook_url = get_config().WOA_URL + robot[u"hook_key"]
            # logger.info(f"key:{self.robot_key},chatid:{self.chatid},hook:{hook_url}")
            bots.add_bot(robot["robot_key"], robot["user_id"], hook_url)
            # 返回信息
            title = "🎉<font color='#1E90FF'>注册成功</font>"
            info = "📖 请通过@与我聊天 \n\n " 
            info = info + "- 更多信息请使用<font color='#1E90FF'>%help%</font> 命令获取"
            message = {
                "msgtype": "markdown",
                "markdown": {
                    "text": f"#### {title}  \n\n {info}"
                }
            }
            return (message , None), BotStatus.REGISTERED
        
        return (message , None),BotStatus.UNREGISTERED