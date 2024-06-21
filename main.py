import base64
import os
import random
import time
import datetime
import logging
import json
from tls_client import Session
 
def load_config():
    required_keys = ["token", "avatars_dir", "log_file", "min_delay", "max_delay"]
    config = {}

    if os.path.exists('config.json'):
        with open('config.json', 'r') as file:
            config = json.load(file)

    if "min_delay" in config:
        try:
            min_delay = int(config["min_delay"])
            if min_delay < 300:
                print("Current min_delay is too low and could risk a ban. It must be at least 5 minutes (300 seconds).")
                config["min_delay"] = input_new_min_delay()
        except ValueError:
            print("min_delay in config is not a valid integer.")
            config["min_delay"] = input_new_min_delay()

    missing_keys = [key for key in required_keys if key not in config]
    for key in missing_keys:
        config[key] = input_value_for_key(key)

    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)

    return config

def input_new_min_delay():
    while True:
        value = input("Enter a new value for min_delay (minimum 300 seconds): ")
        try:
            value = int(value)
            if value >= 300:
                return value
            else:
                print("Minimum delay must be at least 5 minutes (300 seconds) or you could risk a ban.")
        except ValueError:
            print("Please enter a valid integer for min_delay.")

def input_value_for_key(key):
    while True:
        value = input(f"Enter value for {key}: ")
        if key == "min_delay":
            try:
                value = int(value)
                if value < 300:
                    print("Minimum delay must be at least 5 minutes (300 seconds) or you could risk a ban.")
                    continue
            except ValueError:
                print("Please enter a valid integer for min_delay.")
                continue
        return value

config = load_config()

logger = logging.getLogger("log")
logger.setLevel(logging.INFO)

avatars_dir = config["avatars_dir"]

os.makedirs(avatars_dir, exist_ok=True)

if not logger.handlers:
    fh = logging.FileHandler(config["log_file"])
    fh.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(fh)
    logger.addHandler(ch)
    
while True:
	sesh = Session(client_identifier="chrome_115", random_tls_extension_order=True)
	token = config["token"]

	avatar_files = os.listdir(avatars_dir)
	if avatar_files:  # Checks if the list is not empty
			random_avatar_file = random.choice(avatar_files)
			path = os.path.join(avatars_dir, random_avatar_file)
	else:
			print("No avatar files found.")
			break
	
	headers = {
					"authority": "discord.com",
					"method": "PATCH",
					"scheme": "https",
					"accept": "*/*",
					"accept-encoding": "gzip, deflate, br",
					"accept-language": "en-US",
					"authorization": token,
					"origin": "https://discord.com",
					"sec-ch-ua": '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
					"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9020 Chrome/108.0.5359.215 Electron/22.3.26 Safari/537.36",
					"sec-ch-ua-mobile": "?0",
					"sec-ch-ua-platform": '"Windows"',
					"sec-fetch-dest": "empty",
					"sec-fetch-mode": "cors",
					"sec-fetch-site": "same-origin",
					"X-Debug-Options": "bugReporterEnabled",
					"X-Discord-Locale": "en-US",
					"X-Discord-Timezone": "Asia/Calcutta",
					"X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDIwIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMjAgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMjYgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMjYiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNDAyMzcsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM4NTE3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9"
			}
	
	payload = {
			"avatar": f"data:image/jpeg;base64,{base64.b64encode(open(path, 'rb').read()).decode()}"
	}
	
	r = sesh.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)

	current_time = datetime.datetime.now().strftime("%H:%M:%S")

	if r.status_code == 200:
			logger.info(f"{current_time} - Profile picture changed successfully to {random_avatar_file}")
	else:
			logger.info(f"{current_time} - Error: {r.status_code} - Avatar: {path}")

	sleep_duration = random.randint(300, 1200)
	minutes, seconds = divmod(sleep_duration, 60)
	logger.info(f"{current_time} - Waiting for {minutes} minutes and {seconds} seconds before the next change.")
	time.sleep(sleep_duration)