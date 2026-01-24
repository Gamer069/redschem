import discord
from discord.ext import commands

import db
import env
import config

if config.DEV == "true":
    import os

    if os.path.exists(env.SYNC_FLAG):
        os.remove(env.SYNC_FLAG)

    pass

# create intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def setup_hook():
    if config.DEV:
        guild = discord.Object(id=config.GUILD_ID)
        bot.tree.copy_global_to(guild=guild)
        # await bot.tree.sync(guild=guild)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

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
        print(f"ERR: an unexpected error occurred when processing message {msg.id}: {e}")

    await bot.process_commands(msg)


@bot.tree.command(name="resync", description="perform full resync of database \n!!! DROPS TABLE BEFORE SYNCING !!! DESTRUCTIVE.")
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
