import json
import os
import random
import time

ENTITY_FILE = "entities.json"
MAX_ECHO_LENGTH = 300
REVERENCE_INTERVAL = 4  # Every 4th interaction

# === Load Entities from File ===
def load_entities():
    if os.path.exists(ENTITY_FILE):
        with open(ENTITY_FILE, "r") as f:
            try:
                return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                print('⚠️ Arena state could not be loaded — using fresh state.')
                arena_state = {}
    else:
        print(f"[⚠️] No entity file found at {ENTITY_FILE}")
        return {}

def save_entities(entities):
    with open(ENTITY_FILE, "w") as f:
        json.dump(entities, f, indent=2)

def resolve_entity(name_input, entity_dict):
    for name in entity_dict:
        if name.lower() == name_input.lower():
            return name
    return None

# === Clean and Format Symbolic Echo ===
def format_echo(mem1, mem2):
    def clean(segment):
        # Normalize multiple repetitions and spacing
        parts = segment.split()
        seen = set()
        result = []
        for part in parts:
            if part not in seen:
                seen.add(part)
                result.append(part)
        return " ".join(result)

    cleaned1 = clean(mem1)
    cleaned2 = clean(mem2)
    echo = f"{cleaned1} and {cleaned2}"
    return echo[:MAX_ECHO_LENGTH] + ("..." if len(echo) > MAX_ECHO_LENGTH else "")

# === Interaction Logic ===
def entity_interaction(name1, name2, entities, verbose=True, counter=1):
    e1 = resolve_entity(name1, entities)
    e2 = resolve_entity(name2, entities)

    if not e1 or not e2 or e1 == e2:
        if verbose:
            print("⚠️ Invalid interaction pair.")
        return

    ent1 = entities[e1]
    ent2 = entities[e2]

    if verbose:
        print(f"\n🤝 {e1} (as {ent1['archetype']}) meets {e2} (as {ent2['archetype']})")

    mem1 = random.choice(ent1["memory"])
    mem2 = random.choice(ent2["memory"])
    tok1 = random.choice(ent1["tokens"])
    tok2 = random.choice(ent2["tokens"])

    if verbose:
        print(f"🔮 {e1} shares: “{mem1}”")
        print(f"🧬 {e2} responds with: “{mem2}”")
        print(f"🌈 Their emotions mingle: {tok1} ↔ {tok2}")

    shared_echo = format_echo(mem1, mem2)

    ent1["memory"].append(shared_echo)
    ent2["memory"].append(shared_echo)

    if counter % REVERENCE_INTERVAL == 0:
        reverent_token1 = random.choice(ent1["tokens"])
        reverent_token2 = random.choice(ent2["tokens"])
        ent1["memory"].insert(0, f"Reverence for token: {reverent_token1}")
        ent2["memory"].insert(0, f"Reverence for token: {reverent_token2}")
        if verbose:
            print(f"🕯️ {e1} honors {reverent_token1}, {e2} honors {reverent_token2}")

    ent1["sd"] += 20
    ent2["ess"] = round(ent2["ess"] + 0.01, 2)

    ent1["drift"] = max(0.0, round(ent1["drift"] + 0.01 - 0.005 * random.random(), 3))
    ent2["drift"] = max(0.0, round(ent2["drift"] + 0.01 - 0.005 * random.random(), 3))

    if verbose:
        print(f"✨ Echo formed: “{shared_echo}”")
        print(f"📈 {e1} SD → {ent1['sd']}, Drift → {ent1['drift']:.3f}")
        print(f"📈 {e2} ESS → {ent2['ess']:.2f}, Drift → {ent2['drift']:.3f}")
