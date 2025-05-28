
import os
import json

SOURCE_FILE = "entities.json"
DEST_DIR = "entity_data"

def main():
    if not os.path.exists(SOURCE_FILE):
        print(f"❌ Source file '{SOURCE_FILE}' not found.")
        return

    with open(SOURCE_FILE, "r") as f:
        try:
            all_entities = json.load(f)
        except Exception as e:
            print(f"❌ Failed to parse JSON: {e}")
            return

    os.makedirs(DEST_DIR, exist_ok=True)

    for eid, data in all_entities.items():
        data["id"] = eid  # Ensure ID is included
        path = os.path.join(DEST_DIR, f"{eid}.json")
        with open(path, "w") as out:
            json.dump(data, out, indent=2)
        print(f"✅ Imported: {eid} → {path}")

    print(f"✅ All entities imported to '{DEST_DIR}/'")

if __name__ == "__main__":
    main()
