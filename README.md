# RemovePaywalls Bot

A minimal Discord bot that automatically bypasses article paywalls using [removepaywalls.com](https://removepaywalls.com).

> **Disclaimer**: This project is not affiliated with, endorsed by, or connected to removepaywalls.com in any way. It simply uses their public service to generate bypass links.

## Features

- **Auto-detection**: Post a URL from a tracked paywall site, get an automatic bypass link with rich embed preview
- **Manual bypass**: Use `/bypass <url>` for any article
- **Domain management**: Add/remove tracked domains with `/paywalls add|remove|list`

## Setup

### 1. Create Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and name it
3. Go to "Bot" section, click "Add Bot"
4. Enable **Message Content Intent** under Privileged Gateway Intents
5. Copy the bot token

### 2. Install Dependencies

#### Using `uv` (Recommended)

The bot uses inline script dependencies (PEP 723), so you can run it directly with `uv`:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run the bot (uv will handle dependencies automatically)
./bot.py
# or: uv run python bot.py
```

#### Using pip (Alternative)

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or: source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 3. Configure

Create a `.env` file:

```bash
DISCORD_TOKEN=your_discord_bot_token_here
```

### 4. Run

```bash
# Using uv (recommended)
./bot.py

# Or with Python
python bot.py
```

## Docker Deployment

### Using Docker Compose (Recommended)

1. Create a `.env` file with your Discord token:
   ```bash
   DISCORD_TOKEN=your_discord_bot_token_here
   ```

2. Create the data directory (for persistent domain storage):
   ```bash
   mkdir -p data
   ```

3. Build and run:
   ```bash
   docker-compose up -d
   ```

3. View logs:
   ```bash
   docker-compose logs -f
   ```

### Using Docker directly

1. Build the image:
   ```bash
   docker build -t removepaywalls-bot .
   ```

2. Run the container:
   ```bash
   mkdir -p data
   docker run -d \
     --name removepaywalls-bot \
     --restart unless-stopped \
     -e DISCORD_TOKEN=your_discord_bot_token_here \
     -v $(pwd)/data/paywalled_domains.json:/app/paywalled_domains.json \
     removepaywalls-bot
   ```

### 5. Invite Bot to Server

Generate invite URL in Developer Portal → OAuth2 → URL Generator:
- **Scopes**: `bot`, `applications.commands`
- **Permissions**: `Send Messages`, `Read Message History`, `Embed Links`

## Commands

| Command | Description |
|---------|-------------|
| `/bypass <url>` | Bypass paywall for any URL |
| `/paywalls list` | Show tracked domains |
| `/paywalls add <domains>` | Add domain(s), space-separated |
| `/paywalls remove <domains>` | Remove domain(s) |

## How It Works

Uses [removepaywalls.com](https://removepaywalls.com) which searches web archives (Archive.is, Wayback Machine, Google cache) for full article content.

**Limitations**: Won't work for "hard paywalls" where content isn't loaded until login.

## Known Limitations

This bot was written for a small server with trusted users. If deploying to a larger or public server, be aware:

- **No permission checks** — Any user can add/remove tracked domains
- **No rate limiting** — Users could spam URLs and trigger many outbound requests
- **HTTP session per request** — Not optimized for high volume
- **Sync file I/O** — Domain list uses blocking file operations
- **HTML entities** — OG metadata may contain unescaped HTML entities

For production use with untrusted users, consider adding role-based permissions and rate limiting.

## License

MIT
