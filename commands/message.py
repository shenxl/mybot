from .executor import CommandStrategy

class MessageCommandStrategy(CommandStrategy):
    def execute(self, command_arg):
        username = self.rebot["userID"]
        return f'{username}say:{command_arg}'