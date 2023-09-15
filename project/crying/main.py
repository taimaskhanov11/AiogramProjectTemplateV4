import asyncio
from pprint import pformat

from aiogram import Bot, F, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from project.crying import setup
from project.crying.config import Settings


async def on_startup(bot: Bot):
    username = (await bot.me()).username
    logger.warning(f"Bot @{username} started")


async def on_shutdown():
    pass


async def main():
    # Parse command line arguments
    cli_settings = setup.parse_args()
    cli_settings.update_settings(Settings)

    # Initialize logging
    setup.init_logging(cli_settings.log)

    # Initialize settings
    settings = Settings()
    logger.info(f"Settings:\n{pformat(settings.model_dump())}")

    # Initialize database
    session_maker = await setup.init_db(settings.db)

    # Initialize translator
    translator_hub = setup.init_translator_hub()

    # Initialize bot, storage and dispatcher
    bot = Bot(
        token=settings.bot.token.get_secret_value(),
        parse_mode="html"
    )
    storage = MemoryStorage()
    dp = Dispatcher(
        storage=storage,
        settings=settings,
        translator_hub=translator_hub,
    )

    # Register startup and shutdown handlers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Setup filter for private messages only
    dp.message.filter(F.chat.type == "private")

    # Setup routers
    await setup.setup_routers(dp, settings)

    # Setup middlewares
    setup.setup_middlewares(dp, session_maker)

    # Setup scheduler
    scheduler = setup.setup_scheduler()

    # Set bot commands
    await setup.set_commands(bot, settings)

    # Start bot
    try:
        if not cli_settings.webhook:
            logger.info("Start bot in polling mode")
            await bot.delete_webhook()
            await dp.start_polling(
                bot,
                skip_updates=True,
                allowed_updates=dp.resolve_used_update_types(),
                scheduler=scheduler,
            )

        else:
            logger.info("Start bot in webhook mode")
            await setup.start_webhook(bot, dp, settings)

    finally:
        await bot.session.close()
        await dp.storage.close()
        await setup.close_db()


if __name__ == "__main__":
    try:
        try:
            import uvloop

            with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
                runner.run(main())
        except ImportError:
            logger.warning("uvloop is not installed")
            asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
