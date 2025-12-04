"""Paywall bypass cog - auto-detection and slash commands."""

import logging
import re
from urllib.parse import urlparse

import aiohttp
import discord
import tldextract
from discord import app_commands
from discord.ext import commands

import config

log = logging.getLogger(__name__)

# HTTP status constants
HTTP_OK = 200

# Simple URL pattern - matches http(s)://...
URL_PATTERN = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)

# Open Graph meta tag patterns
OG_PATTERNS = {
    "title": re.compile(
        r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\']*)["\']',
        re.IGNORECASE,
    ),
    "description": re.compile(
        r'<meta[^>]*property=["\']og:description["\'][^>]*content=["\']([^"\']*)["\']',
        re.IGNORECASE,
    ),
    "image": re.compile(
        r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']*)["\']',
        re.IGNORECASE,
    ),
    "site_name": re.compile(
        r'<meta[^>]*property=["\']og:site_name["\'][^>]*content=["\']([^"\']*)["\']',
        re.IGNORECASE,
    ),
}
# Fallback patterns (content before property)
OG_PATTERNS_ALT = {
    "title": re.compile(
        r'<meta[^>]*content=["\']([^"\']*)["\'][^>]*property=["\']og:title["\']',
        re.IGNORECASE,
    ),
    "description": re.compile(
        r'<meta[^>]*content=["\']([^"\']*)["\'][^>]*property=["\']og:description["\']',
        re.IGNORECASE,
    ),
    "image": re.compile(
        r'<meta[^>]*content=["\']([^"\']*)["\'][^>]*property=["\']og:image["\']',
        re.IGNORECASE,
    ),
    "site_name": re.compile(
        r'<meta[^>]*content=["\']([^"\']*)["\'][^>]*property=["\']og:site_name["\']',
        re.IGNORECASE,
    ),
}


def extract_domain(url: str) -> str | None:
    """Extract the registered domain from a URL."""
    extracted = tldextract.extract(url)
    return extracted.domain.lower() if extracted.domain else None


def is_valid_url(url: str) -> bool:
    """Check if string is a valid URL."""
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except (ValueError, AttributeError):
        return False


def bypass_url(url: str) -> str:
    """Generate the removepaywalls.com bypass URL."""
    return f"{config.BYPASS_URL}/{url}"


async def fetch_og_metadata(url: str) -> dict[str, str | None]:
    """Fetch Open Graph metadata from a URL."""
    metadata = {"title": None, "description": None, "image": None, "site_name": None}

    try:
        async with aiohttp.ClientSession() as session:
            headers = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1)"}
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.get(url, headers=headers, timeout=timeout) as resp:
                if resp.status != HTTP_OK:
                    return metadata
                # Only read first 50KB to find meta tags
                html = await resp.text(errors="ignore")
                html = html[:50000]
    except (aiohttp.ClientError, aiohttp.ClientTimeout) as e:
        log.debug("Failed to fetch OG metadata from %s: %s", url, e)
        return metadata

    # Extract OG tags
    for key, pattern in OG_PATTERNS.items():
        match = pattern.search(html)
        if not match:
            match = OG_PATTERNS_ALT[key].search(html)
        if match:
            metadata[key] = match.group(1).strip()

    return metadata


def build_embed(url: str, metadata: dict[str, str | None]) -> discord.Embed:
    """Build a Discord embed mimicking a link preview."""
    bypass = bypass_url(url)

    embed = discord.Embed(
        title=metadata.get("title") or "Read Article",
        url=bypass,
        description=metadata.get("description"),
        color=0x5865F2,  # Discord blurple
    )

    if metadata.get("site_name"):
        embed.set_author(name=metadata["site_name"])

    if metadata.get("image"):
        embed.set_thumbnail(url=metadata["image"])

    embed.set_footer(text="via removepaywalls.com")

    return embed


class PaywallCog(commands.Cog):
    """Paywall bypass functionality."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the paywall cog."""
        self.bot = bot
        self.domains = config.load_domains()

    # --- Auto-detection listener ---

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """Auto-detect paywalled URLs in messages and respond with bypass links."""
        # Ignore bots
        if message.author.bot:
            return

        # Find URLs in message
        urls = URL_PATTERN.findall(message.content)
        if not urls:
            return

        # Check each URL against paywalled domains
        for url in urls:
            domain = extract_domain(url)
            if domain and domain in self.domains:
                metadata = await fetch_og_metadata(url)
                embed = build_embed(url, metadata)
                await message.reply(embed=embed, mention_author=False)
                log.info(
                    "Auto-bypassed %s URL for %s",
                    domain,
                    message.author,
                )
                break  # One bypass per message

    # --- Slash commands ---

    @app_commands.command(name="bypass", description="Bypass paywall for any URL")
    @app_commands.describe(url="The article URL to bypass")
    async def bypass(
        self,
        interaction: discord.Interaction,
        url: str,
    ) -> None:
        """Bypass paywall for any provided URL."""
        # Add https:// if no scheme provided
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"

        if not is_valid_url(url):
            await interaction.response.send_message(
                "Invalid URL.",
                ephemeral=True,
            )
            return

        await interaction.response.defer()
        metadata = await fetch_og_metadata(url)
        embed = build_embed(url, metadata)
        await interaction.followup.send(embed=embed)
        log.info("/bypass used by %s for %s", interaction.user, url)

    # --- Paywalls command group ---

    paywalls = app_commands.Group(
        name="paywalls",
        description="Manage paywalled domains",
    )

    @paywalls.command(
        name="list",
        description="List all tracked paywall domains",
    )
    async def paywalls_list(self, interaction: discord.Interaction) -> None:
        """List all tracked paywall domains."""
        if not self.domains:
            await interaction.response.send_message(
                "No domains tracked.",
                ephemeral=True,
            )
            return

        # Format in columns
        sorted_domains = sorted(self.domains)
        domain_list = "  ".join(sorted_domains)
        await interaction.response.send_message(
            f"**Tracked domains ({len(self.domains)}):**\n```\n{domain_list}\n```",
            ephemeral=True,
        )

    @paywalls.command(name="add", description="Add domain(s) to the paywall list")
    @app_commands.describe(
        domains="Domain(s) to add, space-separated (e.g., 'nytimes wsj')",
    )
    async def paywalls_add(
        self,
        interaction: discord.Interaction,
        domains: str,
    ) -> None:
        """Add domain(s) to the tracked paywall list."""
        new_domains = {d.strip().lower() for d in domains.split() if d.strip()}
        if not new_domains:
            await interaction.response.send_message(
                "No valid domains provided.",
                ephemeral=True,
            )
            return

        added = new_domains - self.domains
        self.domains.update(new_domains)
        config.save_domains(self.domains)

        if added:
            await interaction.response.send_message(
                f"Added: `{', '.join(sorted(added))}`",
            )
            log.info("%s added domains: %s", interaction.user, added)
        else:
            await interaction.response.send_message(
                "Those domains are already tracked.",
                ephemeral=True,
            )

    @paywalls.command(
        name="remove",
        description="Remove domain(s) from the paywall list",
    )
    @app_commands.describe(domains="Domain(s) to remove, space-separated")
    async def paywalls_remove(
        self,
        interaction: discord.Interaction,
        domains: str,
    ) -> None:
        """Remove domain(s) from the tracked paywall list."""
        to_remove = {d.strip().lower() for d in domains.split() if d.strip()}
        if not to_remove:
            await interaction.response.send_message(
                "No valid domains provided.",
                ephemeral=True,
            )
            return

        removed = to_remove & self.domains
        self.domains -= to_remove
        config.save_domains(self.domains)

        if removed:
            await interaction.response.send_message(
                f"Removed: `{', '.join(sorted(removed))}`",
            )
            log.info("%s removed domains: %s", interaction.user, removed)
        else:
            await interaction.response.send_message(
                "Those domains weren't being tracked.",
                ephemeral=True,
            )


class ErrorHandler(commands.Cog):
    """Global error handler for the bot."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the error handler."""
        self.bot = bot
        bot.tree.on_error = self.on_app_command_error

    async def on_app_command_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        """Handle slash command errors."""
        if isinstance(error, app_commands.CommandOnCooldown):
            msg = f"Cooldown: try again in {error.retry_after:.1f}s"
        elif isinstance(error, app_commands.MissingPermissions):
            msg = "You don't have permission to use this command."
        else:
            log.exception(
                "Unhandled error in %s: %s",
                interaction.command,
                error,
            )
            msg = "Something went wrong. Please try again."

        if interaction.response.is_done():
            await interaction.followup.send(msg, ephemeral=True)
        else:
            await interaction.response.send_message(msg, ephemeral=True)

    @commands.Cog.listener()
    async def on_command_error(
        self,
        ctx: commands.Context,  # noqa: ARG002
        error: commands.CommandError,
    ) -> None:
        """Handle prefix command errors (if any)."""
        log.exception("Command error: %s", error)


async def setup(bot: commands.Bot) -> None:
    """Set up the paywall cog and error handler."""
    await bot.add_cog(PaywallCog(bot))
    await bot.add_cog(ErrorHandler(bot))
