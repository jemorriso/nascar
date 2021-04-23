import requests
from datetime import datetime
import time

indy_url = "http://racecontrol.indycar.com/xml/timingscoring.json"
while True:
    res = requests.get(indy_url)

    dt = datetime.now()
    with open(f"data/indy-{dt}.txt", "w+") as f:
        print(f"{dt}: writing file...")
        f.write(res.text)

    time.sleep(5)
