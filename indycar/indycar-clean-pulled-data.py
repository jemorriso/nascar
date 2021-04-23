import json
from pathlib import Path
import re


def get_json(text):
    # Using greedy matching because I know I want the LAST closing parens to match, and
    # not any intermediate ones.
    json_text = re.search(r"\((.*)\)", text, flags=re.DOTALL).group(1)
    return json.loads(json_text)
    pass


text_path = Path("indycar/data/txt")
json_path = Path("indycar/data/json")

fs = text_path.iterdir()
for fname in fs:
    print(fname)
    text = fname.read_text()
    indy_json = get_json(text)
    with open(f"{json_path}/{fname.stem}.json", "w+") as f:
        json.dump(indy_json, f, indent=2)
