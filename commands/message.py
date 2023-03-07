from .executor import CommandStrategy

class MessageCommandStrategy(CommandStrategy):
    def execute(self, command_arg):
        return command_arg