import asyncio
from telegram import Bot
from src.config import Config

class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
        self.chat_id = Config.TELEGRAM_CHAT_ID
    
    async def send_message_async(self, text: str):
        await self.bot.send_message(chat_id=self.chat_id, text=text)
    
    def sync_send(self, text: str):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Running in async environment (e.g., Jupyter)
                import nest_asyncio
                nest_asyncio.apply()
                loop.run_until_complete(self.send_message_async(text))
            else:
                loop.run_until_complete(self.send_message_async(text))
        except RuntimeError:
            # No event loop, create a new one
            asyncio.run(self.send_message_async(text))
