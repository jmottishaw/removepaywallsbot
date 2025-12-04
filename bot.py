#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "discord.py==2.6.4",
#     "python-dotenv==1.2.1",
#     "tldextract==5.3.0",
#     "aiohttp==3.13.2",
#     "PyNaCl==1.5.0",
# ]
# ///

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

    def __init__(self) -> None:
        """Initialize the bot with required intents."""
        intents = discord.Intents.default()
        intents.message_content = True  # Required for auto-detection
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self) -> None:
        """Load cogs and sync commands before bot starts."""
        await self.load_extension("cogs.paywall")
        await self.tree.sync()
        log.info("Slash commands synced")

    async def on_ready(self) -> None:
        """Log bot connection status when ready."""
        log.info(
            "Logged in as %s (ID: %s)",
            self.user,
            self.user.id if self.user else "unknown",
        )
        log.info("Connected to %s guild(s)", len(self.guilds))


async def main() -> None:
    """Run the bot."""
    bot = PaywallBot()
    async with bot:
        await bot.start(config.get_token())


if __name__ == "__main__":
    asyncio.run(main())
