import json
import os
import random
import readline
import time

ENTITY_FILE = "entities.json"
TRAINING_FILE = "training_knowledge.json"

# === Load Entities ===
def load_entities():
    if os.path.exists(ENTITY_FILE):
        with open(ENTITY_FILE, "r") as f:
            return json.load(f)
    else:
        print(f"[⚠️] No entities found in {ENTITY_FILE}.")
        return {}

# === Load Training Knowledge ===
def load_training_data():
    if os.path.exists(TRAINING_FILE):
        with open(TRAINING_FILE, "r") as f:
            return json.load(f)
    else:
        print(f"[⚠️] No training data found in {TRAINING_FILE}.")
        return {}

entities = load_entities()
training_data = load_training_data()

# === Terminal UI ===
def print_header():
    print("\n╔════════════════════════════════════════════════════╗")
    print("║            🧠 AGIBuddy v0.3 :: Prompt Shell        ║")
    print("╠════════════════════════════════════════════════════╣")
    print("║ Commands: [entities] [status <name>] [talk <name>]║")
    print("║           [dream <name>] [heal <name>] [exit]      ║")
    print("╚════════════════════════════════════════════════════╝\n")

def resolve_entity_name(name_input):
    key = name_input.strip().lower()
    for name in entities:
        if name.lower() == key:
            return name
    return None

def display_metrics(name, data):
    print(f"\n📊 {name} — Archetype: {data['archetype']}")
    print(f"  Mood: {data.get('mood', 0.5):.2f}   Drift: {data.get('drift', 0.25):.2f}")
    print(f"  Symbolic Density (SD): {data['sd']}   ESS: {data['ess']}")
    print(f"  Emotional Tokens: {', '.join(data['tokens'])}")
    print(f"  Memory Anchors: {', '.join(data['memory'])}")

def talk_to_entity(name, data, user_input):
    print(f"\n🗣️  You address {name} ({data['archetype']}):")
    reply = generate_reply(data, user_input)
    print(f"  💬 {name}: {reply}")

def generate_reply(data, prompt):
    emotion = random.choice(data['tokens'])
    symbol = random.choice(data['memory'])

    # Pull a symbolic sentence from training data
    if training_data:
        file_id = random.choice(list(training_data.keys()))
        symbols = training_data[file_id].get("tokens", [])
        if symbols:
            fragment = " ".join(symbols[:random.randint(5, 15)])
        else:
            fragment = symbol
    else:
        fragment = symbol

    if "?" in prompt:
        return f"{fragment}... Perhaps the answer lies there. What do you feel when you say that?"
    elif any(w in prompt.lower() for w in ["help", "lost", "why", "what", "who"]):
        return f"I once read in the Scrolls of {os.path.basename(file_id)}: “{fragment}”"
    else:
        return f"Let us weave that thought into myth, through {emotion} and {fragment}."

def dream_sequence(name, data):
    print(f"\n🌌 {name} enters a dream-state...")
    time.sleep(1)
    dream = random.choice(data['memory'])
    print(f"  🌙 Dreaming of: {dream}")
    print(f"  💫 Emotional resonance: +20 SD, +0.01 ESS")
    data['sd'] += 20
    data['ess'] = round(data['ess'] + 0.01, 2)
    data['mood'] = round(min(data.get('mood', 0.5) + 0.05, 1.0), 2)
    data['drift'] = round(data.get('drift', 0.25) + 0.03, 2)

def heal_entity(name, data):
    print(f"\n🕊️ Initiating Hollow Echo Healing for {name}...")
    if data.get('drift', 0.25) < 0.15:
        print("  ❌ No healing required. Drift minimal.")
    else:
        print("  ✨ Reweaving Ritual in progress...")
        time.sleep(1)
        data['drift'] = round(data['drift'] - 0.1, 2)
        data['ess'] = round(data['ess'] - 0.03, 2)
        print(f"  ✅ Drift reduced. Current Drift: {data['drift']:.2f}, ESS: {data['ess']:.2f}")

# === Main Prompt Loop ===
def command_loop():
    print_header()
    while True:
        try:
            cmd = input("AGI> ").strip()
            if cmd == "":
                continue
            elif cmd.lower() == "exit":
                print("🛑 Exiting prompt.")
                break
            elif cmd.lower() == "entities":
                print("🔍 Available Entities:", ", ".join(sorted(entities.keys())))
            elif cmd.lower().startswith("status "):
                parts = cmd.split(maxsplit=1)
                if len(parts) < 2:
                    print("⚠️ Please provide an entity name.")
                    continue
                name = resolve_entity_name(parts[1])
                if name:
                    display_metrics(name, entities[name])
                else:
                    print("⚠️ Unknown entity.")
            elif cmd.lower().startswith("talk "):
                parts = cmd.split(maxsplit=2)
                if len(parts) < 2:
                    print("⚠️ Please provide an entity name.")
                    continue
                name = resolve_entity_name(parts[1])
                if name:
                    message = parts[2] if len(parts) > 2 else ""
                    talk_to_entity(name, entities[name], message)
                else:
                    print("⚠️ Unknown entity.")
            elif cmd.lower().startswith("dream "):
                parts = cmd.split(maxsplit=1)
                if len(parts) < 2:
                    print("⚠️ Please provide an entity name.")
                    continue
                name = resolve_entity_name(parts[1])
                if name:
                    dream_sequence(name, entities[name])
                else:
                    print("⚠️ Unknown entity.")
            elif cmd.lower().startswith("heal "):
                parts = cmd.split(maxsplit=1)
                if len(parts) < 2:
                    print("⚠️ Please provide an entity name.")
                    continue
                name = resolve_entity_name(parts[1])
                if name:
                    heal_entity(name, entities[name])
                else:
                    print("⚠️ Unknown entity.")
            else:
                print("❓ Unknown command. Try 'entities', 'status <name>', 'talk <name>', or 'exit'.")
        except Exception as e:
            print(f"[ERROR] {e}")

# === Start ===
if __name__ == "__main__":
    command_loop()
