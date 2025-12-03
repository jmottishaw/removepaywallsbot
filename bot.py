"""Paywall bypass Discord bot - entry point."""

import asyncio
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv

import config

# Load .env file
load_dotenv()

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("paywallbot")


class PaywallBot(commands.Bot):
    """Simple paywall bypass bot."""

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # Required for auto-detection
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        """Called before the bot starts - load cogs and sync commands."""
        await self.load_extension("cogs.paywall")
        await self.tree.sync()
        log.info("Slash commands synced")

    async def on_ready(self):
        """Called when bot is connected and ready."""
        log.info(f"Logged in as {self.user} (ID: {self.user.id})")
        log.info(f"Connected to {len(self.guilds)} guild(s)")


async def main():
    bot = PaywallBot()
    async with bot:
        await bot.start(config.get_token())


if __name__ == "__main__":
    asyncio.run(main())
