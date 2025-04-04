import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django.setup()

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from bot.handlers.user import user


async def main() -> None:
    load_dotenv()
    bot = Bot(token=os.getenv("BOT_TOKEN"),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_routers(user)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped!")
