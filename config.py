"""Configuration management for the paywall bypass bot."""

import json
import os
import shutil
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
# Try data directory first (for Docker), fall back to base directory
DATA_DIR = BASE_DIR / "data"
if DATA_DIR.exists() and DATA_DIR.is_dir():
    DOMAINS_FILE = DATA_DIR / "paywalled_domains.json"
else:
    DOMAINS_FILE = BASE_DIR / "paywalled_domains.json"
DEFAULT_DOMAINS_FILE = BASE_DIR / "domains.txt"

# Service URL
BYPASS_URL = "https://removepaywalls.com"

# Error messages
MISSING_TOKEN_MSG = "DISCORD_TOKEN environment variable not set"  # noqa: S105


def get_token() -> str:
    """Load Discord token from environment variable."""
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError(MISSING_TOKEN_MSG)
    return token


def load_domains() -> set[str]:
    """Load paywalled domains from JSON file, falling back to defaults."""
    # Handle case where Docker created a directory instead of a file
    if DOMAINS_FILE.exists() and DOMAINS_FILE.is_dir():
        shutil.rmtree(DOMAINS_FILE)

    if DOMAINS_FILE.exists() and DOMAINS_FILE.is_file():
        with DOMAINS_FILE.open() as f:
            return set(json.load(f))

    # First run: load from default list
    if DEFAULT_DOMAINS_FILE.exists():
        with DEFAULT_DOMAINS_FILE.open() as f:
            domains = {line.strip().lower() for line in f if line.strip()}
            save_domains(domains)
            return domains

    return set()


def save_domains(domains: set[str]) -> None:
    """Save paywalled domains to JSON file."""
    with DOMAINS_FILE.open("w") as f:
        json.dump(sorted(domains), f, indent=2)
