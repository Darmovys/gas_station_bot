import asyncio
from aiogram import Dispatcher, Bot
from handlers import questions


async def main():
    bot = Bot("Enter your Token API")
    dp = Dispatcher()
    dp.include_router(questions.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())
