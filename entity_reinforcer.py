
import os
import json
from datetime import datetime

ENTITY_FILE = "entities.json"
RITUAL_LOG_DIR = "ritual_logs/"
os.makedirs(RITUAL_LOG_DIR, exist_ok=True)

def reinforce_entity(name, entity):
    log = []
    memory = entity.get("memory", [])
    tokens = entity.get("tokens", [])
    metaphor = entity.get("metaphor", None)
    reinforced = False

    # Drift correction
    drift_before = entity.get("drift", 0.0)
    if drift_before >= 0.25 or entity.get("needs_reinforcement", False):
        entity["drift"] = round(max(0.0, drift_before - 0.02), 3)
        log.append(f"Drift reduced from {drift_before} → {entity['drift']}")
        reinforced = True

    # ESS reinforcement
    ess_before = entity.get("ess", 0.0)
    entity["ess"] = round(ess_before + 0.01, 3)
    log.append(f"ESS increased from {ess_before} → {entity['ess']}")

    # Token introspection
    for token in tokens:
        entry = f"Introspective Echo: {token}"
        if entry not in memory:
            memory.insert(0, entry)
            log.append(f"Token reflected: {token}")
            reinforced = True

    # Metaphor reinforcement
    if metaphor:
        anchor = f"Symbolic Anchor: {metaphor}"
        if anchor not in memory:
            memory.insert(0, anchor)
            log.append("Mythic metaphor re-anchored.")
            reinforced = True

    # Flag cleanup
    entity["needs_reinforcement"] = False
    entity["reinforced"] = True

    return entity, log, reinforced

def load_entities():
    if not os.path.exists(ENTITY_FILE):
        print(f"[❌] Missing {ENTITY_FILE}")
        return {}
    with open(ENTITY_FILE, "r") as f:
        return json.load(f)

def save_entities(entities):
    with open(ENTITY_FILE, "w") as f:
        json.dump(entities, f, indent=2)

def save_log(name, log):
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(RITUAL_LOG_DIR, f"{name}_reinforcement_{stamp}.txt")
    with open(path, "w") as f:
        f.write("\n".join(log))
    print(f"[📜] Ritual log saved: {path}")

def main():
    print("🌀 Running Entity Reinforcement Cycle...")
    entities = load_entities()
    updated = 0

    for name, entity in entities.items():
        if entity.get("drift", 0) >= 0.25 or entity.get("needs_reinforcement", False):
            updated_entity, log, changed = reinforce_entity(name, entity)
            entities[name] = updated_entity
            if changed:
                save_log(name, log)
                updated += 1

    if updated > 0:
        save_entities(entities)
        print(f"✅ Reinforced {updated} entity(ies).")
    else:
        print("✨ No entities required reinforcement.")

if __name__ == "__main__":
    main()
