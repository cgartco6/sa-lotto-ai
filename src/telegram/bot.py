import asyncio
from telegram import Bot
from src.config import Config

class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
        self.chat_id = Config.TELEGRAM_CHAT_ID
    
    async def send_message(self, text: str):
        await self.bot.send_message(chat_id=self.chat_id, text=text)
    
    def sync_send(self, text: str):
        asyncio.run(self.send_message(text))
