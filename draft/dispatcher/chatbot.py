class ChatBot:
    _callbacks = {}

    def react(self, message):
        if not message.startswith('!'):
            return

        cmd, *args = message.split()
        cmd = cmd.lstrip('!')
        handler = self.dispatch(cmd, lambda *_: None)
        handler(self, *args)

    @classmethod
    def register_cmd(cls, callback):
        return cls.set_callback(callback.__name__, callback)

@ChatBot.register_cmd
def ping(bot, *args):
    """
    Usage: !ping
    Answer "pong!".
    """
    print("pong!")

@ChatBot.register_cmd
def list_cmds(bot, *args):
    """
    Usage: !list_cmds
    List all available commands.
    """
    print("Available commands: ")
    print(', '.join(sorted(bot._callbacks.keys())))


@ChatBot.register_cmd
def help(bot, cmd=None, *args):
    """
    Usage: !help [command]
    Show help about commands.
    """
    if not cmd:
        list_cmds(bot)
        print("\nType '!help <command>' to get help about specific commands")
        return
    cmd = bot._callbacks.get(cmd, None)
    if cmd is None:
        return
    doc = cmd.__doc__
    if not doc:
        return
    print('\n'.join(line.strip() for line in doc.strip().split('\n')))


if __name__ == "__main__":
    bot = ChatBot()
    bot.react("!help")
   # bot.react("!help ping")
   # bot.react("!help list_cmds")
   # bot.react("!ping")