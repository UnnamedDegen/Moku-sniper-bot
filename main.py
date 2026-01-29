import requests
import time
import os
from dotenv import load_dotenv
from config import GENERAL_CONFIG, TARGET_CONFIG, MOKU_CONTRACT, API_URL

# Load secrets from .env
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
API_KEY = os.getenv('API_KEY')

seen_items = set()

def send_alert(message, buy_link):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    spacing = "\u00A0" * 60
    final_message = f"{message}\n\n[🛒 BUY PAGE]({buy_link})    {spacing}[@Unnamed_Degen](https://x.com/Unnamed_Degen)"
    
    markup = {"inline_keyboard": [[{"text": "🛒 BUY NOW (MARKET)", "url": buy_link}]]}
    payload = {
        "chat_id": CHAT_ID, "text": final_message, "parse_mode": "Markdown",
        "reply_markup": markup, "disable_web_page_preview": False
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def scan_market(label, max_price, api_rarity, note, custom_emoji, target_name=None):
    headers = {"Content-Type": "application/json", "X-API-Key": API_KEY}
    variables = {
        "tokenAddress": MOKU_CONTRACT, "from": 0, "size": 30, "sort": "PriceAsc",
        "auctionType": "Sale", "criteria": [{"name": "Rarity", "values": [api_rarity]}]
    }
    if target_name:
        variables["name"] = target_name

    query = """
    query GetERC721TokensList($tokenAddress: String, $from: Int!, $size: Int!, $sort: SortBy, $auctionType: AuctionType, $criteria: [SearchCriteria!], $name: String) {
      erc721Tokens(tokenAddress: $tokenAddress, from: $from, size: $size, sort: $sort, auctionType: $auctionType, criteria: $criteria, name: $name) {
        results { tokenId, name, order { currentPrice } }
      }
    }
    """
    try:
        response = requests.post(API_URL, json={'query': query, 'variables': variables}, headers=headers, timeout=15)
        if response.status_code == 200:
            tokens = response.json().get('data', {}).get('erc721Tokens', {}).get('results', [])
            for token in tokens:
                if not token.get('order'): continue
                price_ron = float(token['order']['currentPrice']) / 10**18
                if price_ron <= max_price:
                    alert_id = f"{token['tokenId']}_{price_ron}"
                    if alert_id not in seen_items:
                        buy_link = f"https://marketplace.roninchain.com/collections/{MOKU_CONTRACT}/{token['tokenId']}"
                        mode = f"TARGET: {label}" if target_name else f"GENERAL: {label}"
                        msg = (f"[\u200b]({buy_link}){custom_emoji} *{mode.upper()} DEAL!*\n"
                               f"------------------------------\n"
                               f"👾 *Item:* {token['name']}\n"
                               f"💰 *Price:* {price_ron:.4f} RON\n"
                               f"📝 *Note:* {note}")
                        send_alert(msg, buy_link)
                        seen_items.add(alert_id)
                        print(f"📢 Alert sent: {token['name']} ({price_ron} RON)")
    except Exception as e:
        print(f"Scan error: {e}")

if __name__ == "__main__":
    while True:
        print(f"\n--- [{time.strftime('%H:%M:%S')}] Starting Scan ---")
        for name, limits in TARGET_CONFIG.items():
            for rarity in ["Basic", "Rare", "Epic", "Legendary"]:
                if rarity in limits:
                    scan_market(name, limits[rarity], rarity, "Target price reached!", limits["emoji"], target_name=name)
                    time.sleep(0.4)
        for rarity, conf in GENERAL_CONFIG.items():
            scan_market(rarity, conf["max_price"], conf["api_val"], conf["note"], conf["emoji"])
            time.sleep(0.4)
        time.sleep(15)