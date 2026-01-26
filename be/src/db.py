import asyncpg
import discord

import aiohttp
import gzip
import base64
import json

from typing import Optional
from loguru import logger

import re
import os

import config

from schem import Header, Schem

conn = None


class ImageNotFoundError(Exception):
    pass


async def init_db(DB):

    global conn

    conn = await asyncpg.connect(dsn=DB)

    await conn.execute("""
        CREATE TABLE IF NOT EXISTS schematics (
            id SERIAL PRIMARY KEY,

            category TEXT NOT NULL,
            subcategory TEXT NOT NULL,

            image TEXT NOT NULL,
            schem TEXT NOT NULL,

            title TEXT NOT NULL,
            authors TEXT[] NOT NULL CHECK (array_length(authors, 1) > 0),
            description TEXT NOT NULL,

            input TEXT,
            output TEXT,
            speed TEXT,

            notes TEXT,
            extra_data TEXT
        )
    """)


async def drop():
    await conn.execute("""
        TRUNCATE TABLE schematics RESTART IDENTITY;
    """)


async def parse(bot: discord.Client, msg: discord.Message):
    logger.info("Syncing message {}...", msg.id)

    contents = get_message_contents(msg)
    header = _parse_header(contents)

    subcategory = msg.channel.name
    category = msg.channel.category.name

    schem_data, image_data, extra_data = await _process_attachments(
        msg,
        bot,
        contents
    )

    return Schem(
        header,
        category,
        subcategory,
        schem_data,
        image_data,
        extra_data
    )


def _parse_header(contents: str):
    matches = re.findall(r"```(.*?)```", contents, re.DOTALL)
    if not matches:
        raise ValueError("Message missing header block")
    return Header.parse(matches[0])


async def _process_attachments(
    msg: discord.Message,
    bot: discord.Client,
    contents: str
):
    schem_data = image_data = extra_data = None

    for attachment in get_message_attachments(msg):
        data = await _encode_attachment(attachment)
        name, ext = os.path.splitext(attachment.filename)

        if ext == ".schem":
            schem_data = data
        elif ext.lower() in [".png", ".jpg", ".jpeg", ".gif", ".webp"]:
            image_data = data
        elif ext == "" or ext == ".txt":
            extra_data = data

    if not image_data:
        image_data = await _process_embedded_image(contents, bot)

    if not image_data:
        raise ImageNotFoundError("No image attachment or valid URL found")

    return schem_data, image_data, extra_data


async def _encode_attachment(attachment: discord.Attachment) -> str:
    content_bytes = await attachment.read()
    compressed_bytes = gzip.compress(content_bytes)
    return base64.b64encode(compressed_bytes).decode("utf-8")


async def _process_embedded_image(
    contents: str,
    bot: discord.Client
) -> Optional[str]:
    urls = re.findall(r'(https?://[^\)]+)', contents)
    if not urls:
        return None

    url = await refresh_url(urls[0], bot)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise ImageNotFoundError(f"Downloading image from {url} failed: HTTP {resp.status}")
                img_bytes = await resp.read()

        compressed = gzip.compress(img_bytes)
        return base64.b64encode(compressed).decode("utf-8")
    except aiohttp.ClientError as e:
        raise ImageNotFoundError(f"Downloading image from {url} failed: {e}")


async def full_sync(bot: discord.Client):
    await drop()

    guild = bot.get_guild(config.GUILD_ID)

    for i in config.CHANNELS:
        logger.info("Syncing channel {}...", i)
        channel = discord.utils.get(guild.text_channels, name=i)

        if channel is None:
            logger.error("Channel {} does not exist, skipping...")

        async for msg in channel.history(limit=None):
            if msg.author.bot:
                continue
            msg = await channel.fetch_message(msg.id)
            try:
                schem = await parse(bot, msg)
                await schem.add_to_db(conn)
            except ImageNotFoundError as e:
                logger.warning(
                    "skipping msg {} because image couldn't be processed: {}",
                    msg.id,
                    e
                )
            except Exception as e:
                logger.error(
                    "an unexpected error occurred when processing msg {}: {}",
                    msg.id,
                    e
                )


def get_message_contents(msg) -> str:
    """
    Returns the content of a msg.
    Prefers the msg's own content;falls back to the snapshot if none exists.
    """
    if hasattr(msg, "content") and msg.content:
        return msg.content
    elif getattr(msg, "message_snapshots", None):
        snap = msg.message_snapshots[0]
        return getattr(snap, "content", "")
    return ""


def get_message_attachments(msg) -> list[discord.Attachment]:
    """
    Returns the attachments of a message.
    Prefers the msg's own attachments;falls back to the snapshot if none exist.
    """
    if hasattr(msg, "attachments") and msg.attachments:
        return msg.attachments
    elif getattr(msg, "message_snapshots", None):
        snap = msg.message_snapshots[0]
        return getattr(snap, "attachments", [])
    return []


async def refresh_url(url: str, bot) -> str:
    """
    Refresh a Discord CDN attachment URL.
    Returns the refreshed URL as a string.
    Raises on any failure.
    """
    endpoint = "https://discord.com/api/v10/attachments/refresh-urls"

    headers = {
        "Authorization": f"Bot {bot.http.token}",
        "Content-Type": "application/json",
    }

    payload = {
        "attachment_urls": [url]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, json=payload, headers=headers) as resp:
            text = await resp.text()

            if resp.status != 200:
                raise RuntimeError(
                    f"Failed to refresh URL: HTTP {resp.status} — {text}"
                )

            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                raise RuntimeError(
                    f"Failed to parse JSON from Discord: {text}"
                )

    refreshed = data.get("refreshed_urls")
    if not refreshed:
        raise RuntimeError(f"No refreshed_urls in response: {data}")

    # Map original → refreshed (robust to ordering)
    mapping = {
        item["original"]: item["refreshed"]
        for item in refreshed
        if "original" in item and "refreshed" in item
    }

    new_url = mapping.get(url)
    if not new_url:
        raise RuntimeError(
            "Original URL not found in refresh response.\n"
            f"original={url}\n"
            f"mapping={mapping}"
        )

    return new_url
