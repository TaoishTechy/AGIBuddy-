import json
from pathlib import Path

VILLAGE_DATA_DIR = Path("village_data")

for file in VILLAGE_DATA_DIR.rglob("*.json"):
    with open(file, "r") as f:
        data = json.load(f)

    if isinstance(data.get("buildings"), list):
        print(f"🔧 Fixing building format in: {file.name}")
        data["buildings"] = {}

        with open(file, "w") as f:
            json.dump(data, f, indent=2
