
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
            return json.load(f)
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

    shared_echo = f"{mem1} and {mem2}"
    if len(shared_echo) > MAX_ECHO_LENGTH:
        shared_echo = shared_echo[:MAX_ECHO_LENGTH] + "..."

    ent1["memory"].append(shared_echo)
    ent2["memory"].append(shared_echo)

    # Inject token reverence periodically
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

# === Group Session Logic ===
def group_session(entities, cycles=5):
    names = list(entities.keys())
    print(f"\n🌀 Starting group symbolic recursion — {cycles} cycles")
    counter = 0

    for cycle in range(1, cycles + 1):
        print(f"\n🧭 Cycle {cycle}")
        random.shuffle(names)
        for i in range(0, len(names) - 1, 2):
            counter += 1
            entity_interaction(names[i], names[i+1], entities, verbose=True, counter=counter)
        time.sleep(0.5)

# === CLI Loop ===
def arena_loop():
    entities = load_entities()

    print("\n╔═══════════════════════════════════════╗")
    print("║   🔁 AGIBuddy Entity Arena v0.3.4    ║")
    print("╠═══════════════════════════════════════╣")
    print("║ Commands:                            ║")
    print("║  list            → show entities     ║")
    print("║  interact A B    → symbolic exchange ║")
    print("║  random          → random pair chat  ║")
    print("║  group <cycles>  → group recursion   ║")
    print("║  save            → persist updates   ║")
    print("║  exit            → quit the arena    ║")
    print("╚═══════════════════════════════════════╝")

    while True:
        cmd = input("arena> ").strip().lower()
        if cmd == "list":
            print("🔍 Entities:", ", ".join(sorted(entities.keys())))
        elif cmd.startswith("interact "):
            try:
                _, e1, e2 = cmd.split()
                entity_interaction(e1, e2, entities, counter=random.randint(1, 10))
            except ValueError:
                print("⚠️ Usage: interact <Entity1> <Entity2>")
        elif cmd == "random":
            e1, e2 = random.sample(list(entities.keys()), 2)
            entity_interaction(e1, e2, entities, counter=random.randint(1, 10))
        elif cmd.startswith("group "):
            try:
                _, n = cmd.split()
                cycles = int(n)
                group_session(entities, cycles)
            except ValueError:
                print("⚠️ Usage: group <number_of_cycles>")
        elif cmd == "save":
            save_entities(entities)
            print("💾 Entities updated and saved.")
        elif cmd == "exit":
            print("👋 Leaving arena.")
            break
        else:
            print("❓ Unknown command. Try 'list', 'interact A B', 'random', 'group N', 'save', or 'exit'.")

if __name__ == "__main__":
    arena_loop()
