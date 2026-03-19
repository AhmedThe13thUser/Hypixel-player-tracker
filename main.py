import os
import sys
import time
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from win11toast import notify
import pystray

from PIL import Image

player = None

if len(sys.argv) != 2:
    print("Usage: python main.py <player_name>")
    sys.exit()
else:
    player = sys.argv[1]

s = requests.Session()


# add headers
s.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
})

dt = datetime.now().strftime("%Y-%m-%d %H:%M")
def clear():
    s.cache = None  # Clears the cache for this session
    os.system('cls' if os.name == 'nt' else 'clear')
    return datetime.now().strftime("%Y-%m-%d %H:%M")


# Create tray icon
image = Image.new("RGB", (64, 64), "black")  # Simple placeholder image

icon = pystray.Icon("Console Control", image, "Console Tray Control")

# Run the icon (non-blocking)
icon.run_detached()

while True:
    request = s.get(f"https://plancke.io/hypixel/player/stats/{player}")
    html = request.text
    soup = BeautifulSoup(html, "html.parser")
    # get text inside class class="card-box m-b-10"
    card_box = soup.find_all("div", class_=["card-box", "m-b-10"])
    match = re.search(r'Last Login: .*EST', card_box[0].text, re.IGNORECASE)
    print(f"Last update: {dt}")
    status = card_box[-1].text
    print(status, match.group(0).strip())
    if "offline" not in status.lower():
        notify("Hypixel Status", f"{player} is ONLINE!",audio='ms-winsoundevent:Notification.Looping.Alarm')
        icon.icon = Image.new("RGB", (64, 64), "red")  # Change icon to red when offline
    icon.title = f"{player} - {status.strip()} \n Last update: {dt} \n last login: {match.group(0).strip()}"
    time.sleep(60*10)
    dt = clear()