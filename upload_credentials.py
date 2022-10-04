import os
import json
import subprocess


if not os.path.exists("credentials.json"):
    print("Bruh")
    exit()

with open("credentials.json", 'r') as f:
    credentials = json.loads(f.read())

for key in credentials:
    subprocess.run(["heroku", "config:set", f"{key}='{credentials[key]}'"])
