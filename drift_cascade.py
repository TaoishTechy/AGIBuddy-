
import json
import random

ENTITY_FILE = "entities.json"
CASCADE_LOG = "drift_cascade_log.txt"

def load_entities():
    with open(ENTITY_FILE, "r") as f:
        return json.load(f)

def save_entities(data):
    with open(ENTITY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def simulate_cascade(entities):
    # Guard against unbounded recursion
    MAX_DEPTH = 5
    if 'depth' not in locals():
        depth = 0
    if depth >= MAX_DEPTH:
        return f"⚠️ Max symbolic drift depth reached: {depth}"
    log = ["💥 SIMULATING DRIFT CASCADE..."]
    for name, ent in entities.items():
        old_drift = ent.get("drift", 0.0)
        increase = round(random.uniform(0.02, 0.12), 3)
        ent["drift"] = round(min(1.5, old_drift + increase), 3)
        log.append(f"{name}: Drift {old_drift} → {ent['drift']} (+{increase})")
    return entities, log

def main():
    entities = load_entities()
    entities, log = simulate_cascade(entities)
    save_entities(entities)
    with open(CASCADE_LOG, "w") as f:
        f.write("\n".join(log))
    print("\n".join(log))

if __name__ == "__main__":
    main()
