import json
from pathlib import Path
from civilization.village_engine import Village

# === Persistent Storage Path ===
VILLAGE_DATA_DIR = Path("data/villages")
VILLAGE_DATA_DIR.mkdir(parents=True, exist_ok=True)

# === Save a single village ===
def save_village(village: Village):
    path = VILLAGE_DATA_DIR / f"{village.id}.json"
    with open(path, "w") as f:
        json.dump(village.to_dict(), f, indent=2)
    print(f"[💾] Village '{village.name}' saved to {path}")

# === Load a village by ID ===
def load_village(village_id: str) -> Village:
    path = VILLAGE_DATA_DIR / f"{village_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Village with ID {village_id} not found.")
    with open(path, "r") as f:
        try:
            data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print('⚠️ Village registry failed to load. Starting empty.')
            registry = {}
        return Village.from_dict(data)

# === List all saved villages ===
def list_villages() -> dict:
    villages = {}
    for path in VILLAGE_DATA_DIR.rglob("*.json"):
        try:
            with open(path, "r") as f:
                data = json.load(f)
                villages[data["id"]] = {
                    "name": data.get("name", "Unknown"),
                    "population": data.get("population", 0),
                    "age": data.get("age", 0),
                    "buildings": list(data.get("buildings", {}).keys())
                }
        except Exception as e:
            print(f"[⚠️] Failed to load {path.name}: {e}")
    return villages
