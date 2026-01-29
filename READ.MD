# 🤖 Moku Sniper & Market Tracker

An automated tracking tool for Moku NFTs on the Ronin Network. This bot monitors the marketplace floor and specific NFT names, sending instant alerts to Telegram when prices drop below your targets.

## ✨ Features
* **Dual Monitoring:** Tracks both general rarity floors and specific NFT names simultaneously.
* **Full Rarity Support:** Monitors Basic, Rare, Epic, and Legendary items.
* **Smart Telegram Alerts:** Beautifully formatted messages with direct buy links and social integration.
* **Optimized Performance:** Multi-file structure and rate-limit friendly scanning.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/moku-sniper-bot.git](https://github.com/YOUR_USERNAME/moku-sniper-bot.git)
   cd moku-sniper-bot

2. **Install dependencies:**
   -> pip install requests python-dotenv

3. **Setup Environment Variables: Create a .env file in the root folder with:**
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
API_KEY=your_skymavis_api_key

4. **Run the bot:**
python main.py


## ⚙️ Configuration
You can easily adjust prices, names, and emojis in the config.py file.
