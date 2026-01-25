import discord
from discord.ext import commands

from loguru import logger
import sys

import db
import env
import config

if config.DEV == "true":
    import os

    if os.path.exists(env.SYNC_FLAG):
        os.remove(env.SYNC_FLAG)

    pass


def init_logger():
    """Init loguru logger."""
    logger.remove()

    LOG_FORMAT = (
        "[<green>{time:HH:mm:ss}</green>] "
        "[<level>{level}</level>] "
        "<cyan>{{{name}:{line}}}</cyan> "
        "{message}"
    )

    logger.add(
        sink=sys.stdout,
        format=LOG_FORMAT,
        level="DEBUG",
        filter=lambda record: record["level"].no < 30  # Only DEBUG (10) and INFO (20)
    )

    logger.add(
        sink=sys.stderr,
        format=LOG_FORMAT,
        level="WARNING"  # WARNING (30), ERROR (40), CRITICAL (50)
    )

    logger.add(
        sink="logs/bot_{time:YYYY-MM-DD}.log",
        format=LOG_FORMAT,
        level="DEBUG",
        rotation="00:00",
        retention="7 days"
    )


def init_bot():
    # create intents
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    intents.messages = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    setup_events(bot)


def setup_events(bot):
    @bot.event
    async def setup_hook():
        if config.DEV:
            guild = discord.Object(id=config.GUILD_ID)
            bot.tree.copy_global_to(guild=guild)
            # await bot.tree.sync(guild=guild)

    @bot.event
    async def on_ready():
        logger.info("Logged in as {}", bot.user)

        await db.init_db(config.DB)

        await env.identify_first_run(bot)

    @bot.event
    async def on_message(msg: discord.Message):
        if msg.author.bot:
            return

        if msg.channel.name not in config.CHANNELS:
            return

        try:
            parsed = await db.parse(bot, msg)
            await parsed.add_to_db(db.conn)
        except db.ImageNotFoundError as e:
            await msg.reply(f"Could not process schematic: {e}")
        except Exception as e:
            await msg.reply(f"An unexpected error occurred: {e}")

            logger.error(
                "an unexpected error occurred when processing message {}: {}",
                msg.id, e
            )

        await bot.process_commands(msg)

    setup_commands(bot)


def setup_commands(bot):
    @bot.tree.command(
        name="resync",
        description="Perform full resync of database. "
        "WARNING: Drops table before syncing!"
    )
    @discord.app_commands.default_permissions(manage_messages=True)
    async def resync(ctx: discord.Interaction):
        await ctx.response.defer(ephemeral=True)

        await db.drop()
        await db.full_sync(bot)
        await ctx.followup.send("Performed full resync.", ephemeral=True)

    @bot.tree.command(name="ping", description="ping bot")
    async def ping(ctx: discord.Interaction):
        await ctx.response.send_message("pong")

    bot.run(config.TOKEN)


def main():
    init_logger()
    init_bot()
