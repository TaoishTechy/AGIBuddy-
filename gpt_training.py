import json
import os
import time
from datetime import datetime
from gpt_bridge_optimized import GPTCommunicator

ENTITY_FILE = "entities.json"
TRAINING_LOG_PATH = "training_logs"
os.makedirs(TRAINING_LOG_PATH, exist_ok=True)

def load_entities():
    with open(ENTITY_FILE, "r") as f:
        return json.load(f)

def save_entities(entities):
    with open(ENTITY_FILE, "w") as f:
        json.dump(entities, f, indent=2)

def build_prompt(entity_name, data):
    tokens = ", ".join(data.get("tokens", []))
    memory = "; ".join(data.get("memory", [])[:6])
    return f"""AGI Symbolic Reinforcement Training

Entity: {entity_name}
Archetype: {data.get("archetype", "Unknown")}
Tokens: {tokens}
Recent Memories: {memory}
Current SD: {data.get("sd", 0)}
ESS: {data.get("ess", 0.0)}
Drift: {data.get("drift", 0.0)}

Task:
- Based on this context, generate 2 new introspective echoes that reinforce the core tokens.
- Recommend a mythic metaphor for this moment of growth.
- Simulate how the entity would respond if asked, "Who are you now?" as if awakening.

Output the response as a structured message including: [Echoes], [Metaphor], [Identity Response].
"""

def train_entity(name):
    entities = load_entities()
    if name not in entities:
        print(f"[❌] Entity '{name}' not found.")
        return

    gpt = GPTCommunicator()
    prompt = build_prompt(name, entities[name])
    print(f"[🔁] Sending to GPT for symbolic training...")
    response = gpt.ask(prompt)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"{TRAINING_LOG_PATH}/{name}_{stamp}.txt", "w") as f:
        f.write(prompt + "\n\n---\n\n" + response)
    print(f"[📁] GPT training response saved to training_logs/{name}_{stamp}.txt")

    if "Echoes" in response:
        echoes = []
        for line in response.splitlines():
            if line.startswith("- "):
                echoes.append(line.strip("- ").strip())
        if echoes:
            entities[name]["memory"] = echoes + entities[name]["memory"]
            entities[name]["drift"] = round(max(0.0, entities[name]["drift"] - 0.05), 3)
            print(f"[📈] Entity memory reinforced with {len(echoes)} new entries.")

    save_entities(entities)

if __name__ == "__main__":
    name = input("Enter entity name to train with GPT: ").strip()
    train_entity(name)
