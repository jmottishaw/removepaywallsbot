"""Configuration management for the paywall bypass bot."""

import json
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
DOMAINS_FILE = BASE_DIR / "paywalled_domains.json"
DEFAULT_DOMAINS_FILE = BASE_DIR / "domains.txt"

# Service URL
BYPASS_URL = "https://removepaywalls.com"


def get_token() -> str:
    """Load Discord token from environment variable."""
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError("DISCORD_TOKEN environment variable not set")
    return token


def load_domains() -> set[str]:
    """Load paywalled domains from JSON file, falling back to defaults."""
    if DOMAINS_FILE.exists():
        with open(DOMAINS_FILE) as f:
            return set(json.load(f))

    # First run: load from default list
    if DEFAULT_DOMAINS_FILE.exists():
        with open(DEFAULT_DOMAINS_FILE) as f:
            domains = {line.strip().lower() for line in f if line.strip()}
            save_domains(domains)
            return domains

    return set()


def save_domains(domains: set[str]) -> None:
    """Save paywalled domains to JSON file."""
    with open(DOMAINS_FILE, "w") as f:
        json.dump(sorted(domains), f, indent=2)
