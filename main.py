from bot import bot
from bot.utils import get_discord_bot_token, get_log_handler

if __name__ == "__main__":
    handler = get_log_handler()
    token = get_discord_bot_token()
    bot.run(token=token, log_handler=handler, root_logger=True)
