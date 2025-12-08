# Detailed Setup Guide: Inviting the Bot to Your Discord Server

This guide walks you through the complete process of setting up and inviting the RemovePaywalls bot to your Discord server.

## Prerequisites

- A Discord account
- Administrator permissions on the Discord server you want to add the bot to (or permission to invite bots)
- Python 3.12+ installed (or Docker if using containerized deployment)

---

## Part 1: Create Discord Application & Bot

### Step 1: Access Discord Developer Portal

1. Open your web browser and go to: https://discord.com/developers/applications
2. Log in with your Discord account if prompted

### Step 2: Create a New Application

1. Click the **"New Application"** button (usually in the top right)
2. Enter a name for your application (e.g., "RemovePaywalls Bot")
3. Read and accept the Developer Terms of Service if prompted
4. Click **"Create"**

### Step 3: Create the Bot

1. In the left sidebar, click **"Bot"**
2. Click the **"Add Bot"** button
3. A confirmation dialog will appear - click **"Yes, do it!"**
4. Your bot has been created! You'll see:
   - Bot username
   - Bot icon (you can upload one later)
   - Bot token (this is sensitive - keep it secret!)

### Step 4: Configure Bot Settings

1. **Set Bot Username** (optional):
   - You can change the bot's username in the "Username" field
   - Click **"Save Changes"** if you modify it

2. **Enable Message Content Intent** (REQUIRED):
   - Scroll down to the **"Privileged Gateway Intents"** section
   - Find **"Message Content Intent"**
   - Toggle it **ON** (this is required for the bot to read message content)
   - Click **"Save Changes"** when prompted

3. **Disable Public Bot** (optional, recommended for private use):
   - If you only want this bot in your servers, toggle **"Public Bot"** to **OFF**
   - This prevents others from finding and adding your bot

### Step 5: Copy Your Bot Token

1. In the Bot section, find the **"Token"** section
2. Click **"Reset Token"** if you haven't set one yet, or **"Copy"** if it's already visible
3. **IMPORTANT**: Save this token securely - you'll need it in the next section
   - ⚠️ **Never share this token publicly** - anyone with it can control your bot
   - ⚠️ If you accidentally share it, click "Reset Token" immediately

---

## Part 2: Configure the Bot Locally

### Step 1: Create `.env` File

1. Navigate to your project directory (where `bot.py` is located)
2. Create a new file named `.env` (with the leading dot)
3. Open the file in a text editor
4. Add the following line, replacing `your_discord_bot_token_here` with the token you copied:

```bash
DISCORD_TOKEN=your_discord_bot_token_here
```

**Example:**
```bash
DISCORD_TOKEN=your_actual_bot_token_here
```

5. Save the file

**Note**: Make sure `.env` is in your `.gitignore` file to avoid committing your token to version control!

### Step 2: Verify Setup (Optional)

You can verify your token is set correctly by running:

```bash
# Using uv (recommended)
uv run python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Token set!' if os.getenv('DISCORD_TOKEN') else 'Token missing!')"

# Or with Python
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Token set!' if os.getenv('DISCORD_TOKEN') else 'Token missing!')"
```

---

## Part 3: Generate Invite URL

### Step 1: Navigate to OAuth2 URL Generator

1. In the Discord Developer Portal, click **"OAuth2"** in the left sidebar
2. Click **"URL Generator"** (should be selected by default)

### Step 2: Select Scopes

In the **"Scopes"** section, check the following boxes:

- ✅ **`bot`** - Required for the bot to join servers
- ✅ **`applications.commands`** - Required for slash commands (`/bypass`, `/paywalls`)

### Step 3: Select Bot Permissions

In the **"Bot Permissions"** section, check the following permissions:

**Text Permissions:**
- ✅ **Send Messages** - Bot needs to send bypass links
- ✅ **Read Message History** - Bot needs to read messages to detect paywall URLs
- ✅ **Embed Links** - Bot needs to send rich embed previews

**Optional but Recommended:**
- ✅ **Use Slash Commands** - Already covered by `applications.commands` scope, but good to have

### Step 4: Copy the Generated URL

1. Scroll down to the **"Generated URL"** section
2. You'll see a URL that looks like:
   ```
   https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=PERMISSIONS&scope=bot%20applications.commands
   ```
3. Click **"Copy"** to copy the full URL
4. Save this URL - you'll use it in the next step

---

## Part 4: Invite Bot to Your Server

### Step 1: Open the Invite URL

1. Open a new browser tab or window
2. Paste the invite URL you copied in Part 3, Step 4
3. Press Enter to navigate to the URL

### Step 2: Select Your Server

1. You'll see a Discord authorization page
2. In the **"Add to Server"** dropdown, select the server you want to add the bot to
   - ⚠️ You must have "Manage Server" or "Administrator" permissions on the server
   - ⚠️ If you don't see your server, you don't have permission to add bots

### Step 3: Authorize the Bot

1. Review the permissions the bot is requesting
2. Click **"Authorize"**
3. Complete any CAPTCHA if prompted
4. You should see a success message: "Authorized! You can now close this window."

### Step 4: Verify Bot Joined

1. Open Discord (app or web)
2. Navigate to the server you just added the bot to
3. Check the member list - you should see your bot appear
4. The bot will be offline until you start it (next section)

---

## Part 5: Start the Bot

### Option A: Using `uv` (Recommended)

1. Make sure you have `uv` installed:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Navigate to your project directory:
   ```bash
   cd /path/to/removepaywallsbot
   ```

3. Make the script executable (if on Mac/Linux):
   ```bash
   chmod +x bot.py
   ```

4. Run the bot:
   ```bash
   ./bot.py
   ```
   
   Or:
   ```bash
   uv run python bot.py
   ```

### Option B: Using Python Directly

1. Create a virtual environment (if not already done):
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   ```bash
   # On Mac/Linux:
   source .venv/bin/activate
   
   # On Windows:
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

### Option C: Using Docker

1. Build and run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

2. View logs to verify it's running:
   ```bash
   docker-compose logs -f
   ```

### Verify Bot is Running

When the bot starts successfully, you should see logs like:

```
2024-01-01 12:00:00 | INFO     | paywallbot | Logged in as YourBotName#1234 (ID: 123456789012345678)
2024-01-01 12:00:00 | INFO     | paywallbot | Connected to 1 guild(s)
2024-01-01 12:00:00 | INFO     | paywallbot | Slash commands synced
```

1. Go back to Discord
2. Check the member list - the bot should now show as **online** (green dot)
3. Try typing `/bypass` in a channel - you should see the command appear in the autocomplete

---

## Part 6: Test the Bot

### Test Slash Commands

1. In any channel where the bot can see messages, type `/bypass`
2. You should see the command appear with a URL parameter
3. Try: `/bypass https://example.com/article`
4. The bot should respond with a bypass link

### Test Auto-Detection

1. Post a URL from a paywalled site (if you have one in your tracked domains)
2. The bot should automatically detect it and reply with a bypass link

### Test Domain Management

1. Type `/paywalls list` to see current tracked domains
2. Type `/paywalls add example.com` to add a domain
3. Type `/paywalls list` again to verify it was added

---

## Troubleshooting

### Bot Shows as Offline

- ✅ Check that the bot process is running
- ✅ Check that `DISCORD_TOKEN` is set correctly in `.env`
- ✅ Verify the token hasn't been reset in the Developer Portal
- ✅ Check console/terminal for error messages

### Bot Doesn't Respond to Commands

- ✅ Wait a few minutes after starting - slash commands can take time to sync
- ✅ Make sure the bot has "Use Slash Commands" permission
- ✅ Try restarting the bot
- ✅ Check that you're using `/` commands, not `!` prefix commands

### Bot Can't Read Messages

- ✅ Verify "Message Content Intent" is enabled in Developer Portal → Bot
- ✅ Restart the bot after enabling the intent
- ✅ Check that the bot has "Read Message History" permission

### Bot Can't Send Messages

- ✅ Check that the bot has "Send Messages" permission in the channel
- ✅ Verify the bot's role isn't muted
- ✅ Check channel permissions - the bot needs to be able to send messages

### "Missing Permissions" Error

- ✅ Re-invite the bot with the correct permissions
- ✅ Check server/channel permission overrides
- ✅ Make sure the bot's role is high enough in the role hierarchy

---

## Security Notes

1. **Never commit your `.env` file** - it contains your bot token
2. **Never share your bot token** - anyone with it can control your bot
3. **Reset your token immediately** if it's ever exposed
4. **Use environment variables** in production deployments
5. **Review bot permissions regularly** - only grant what's necessary

---

## Next Steps

- Customize tracked domains using `/paywalls add`
- Set up the bot to run automatically (systemd, PM2, Docker with restart policy, etc.)
- Monitor bot logs for errors
- Consider adding rate limiting if deploying to a public server

---

## Quick Reference

**Developer Portal**: https://discord.com/developers/applications

**Required Scopes**: `bot`, `applications.commands`

**Required Permissions**: Send Messages, Read Message History, Embed Links

**Required Intent**: Message Content Intent

**Environment Variable**: `DISCORD_TOKEN=your_token_here`

