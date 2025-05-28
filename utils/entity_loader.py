import os
import json
from core.entity import Entity

ENTITY_DIR = "entity_data"

def load_entities() -> dict:
    """Load all entities from disk as a dict of {id: Entity instance}."""
    entities = {}
    if not os.path.exists(ENTITY_DIR):
        os.makedirs(ENTITY_DIR)
    for fname in os.listdir(ENTITY_DIR):
        if fname.endswith(".json"):
            path = os.path.join(ENTITY_DIR, fname)
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    e = Entity.from_dict(data)
                    entities[e.id] = e
            except Exception as ex:
                print(f"[⚠️] Failed to load {fname}: {ex}")
    return entities

def load_entity_by_id(eid: str) -> Entity | None:
    path = os.path.join(ENTITY_DIR, f"{eid}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return Entity.from_dict(json.load(f))

def save_entities(entities: dict):
    if not os.path.exists(ENTITY_DIR):
        os.makedirs(ENTITY_DIR)
    for eid, ent in entities.items():
        with open(os.path.join(ENTITY_DIR, f"{eid}.json"), "w") as f:
            json.dump(ent.to_dict(), f, indent=2)
