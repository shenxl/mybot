
class mockBot:
    def __init__(self):
        self.bots = [{"robot_key": "shenxl", "chat_id": 1111, "hook": "hook url"}]

    def get_bot(self, robot_key):
        for bot in self.bots:
            if bot['robot_key'] == robot_key:
                return bot
        return None

    def add_bot(self, robot_key, chat_id, hook):
        new_bot = {"robot_key": robot_key, "chat_id": chat_id, "hook": hook}
        self.bots.append(new_bot)

    

