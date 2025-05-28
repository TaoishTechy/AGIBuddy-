# training_log.py

import json
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def export_entity(entity):
    out = {
        "id": entity.id,
        "archetype": entity.archetype,
        "memory": entity.current_memory,
        "drift": entity.drift_level,
        "status": entity.status,
        "motifs": [frag["text"] for frag in entity.crystal.fragments.values()],
        "emotions": entity.emotion.levels,
        "dream": entity.dream.current_layer,
        "timestamp": datetime.now().isoformat()
    }
    return out

def save_simulation(entities, cycle_id=None):
    payload = [export_entity(e) for e in entities]
    tag = datetime.now().strftime("%Y-%m-%d_%H-%M") if not cycle_id else f"cycle_{cycle_id}"
    path = LOG_DIR / f"AGIBuddy_{tag}.json"
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"📦 Simulation saved to: {path}")
