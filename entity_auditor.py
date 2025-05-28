
import os
import json
from datetime import datetime
from gpt_bridge_optimized import GPTCommunicator, DeepSeekCommunicator

AUDIT_LOG_PATH = "audit_logs/"
ENTITY_FILE = "entities.json"
os.makedirs(AUDIT_LOG_PATH, exist_ok=True)

class EntityAuditor:
    def __init__(self, model="gpt"):
        self.model = model.lower()
        self.gpt = GPTCommunicator()
        self.deepseek = DeepSeekCommunicator()

    def audit_entity(self, entity_name, entity_data, question=None, store=True):
        MAX_AUDIT_DEPTH = 5
        if 'depth' not in locals(): depth = 0
        if depth >= MAX_AUDIT_DEPTH:
            return {'status': '⚠️ Audit recursion limit reached', 'depth': depth}
        prompt = self._build_prompt(entity_name, entity_data, question)
# 📋 Begin Audit Log
        print(f"\n[🔎] Audit Prompt:\n{prompt}\n")

        if self.model == "gpt":
            response = self.gpt.ask(prompt)
        elif self.model == "deepseek":
            response = self.deepseek.ask(prompt)
        else:
            response = "[ERROR] Unknown model."

        # Apply response intelligence
        summary = {"drift_reduction": 0, "ritual": None, "metaphor": None}
        try:
            if "drift" in response.lower() and "yes" in response.lower():
                summary["drift_reduction"] = 0.01
            if "memory ritual" in response.lower() or "reassert" in response.lower():
                summary["ritual"] = "reinforce_tokens"
            if "like a" in response.lower():
                lines = response.splitlines()
                summary["metaphor"] = next((l.strip() for l in lines if "like a" in l.lower()), None)
        except Exception as e:
            print(f"[⚠️] Could not parse audit feedback: {e}")

        # Apply symbolic updates
        if summary["drift_reduction"]:
            old_drift = entity_data.get("drift", 0.0)
            entity_data["drift"] = round(max(0.0, old_drift - summary["drift_reduction"]), 3)
            print(f"↘️ Drift adjusted: {old_drift} → {entity_data['drift']}")
        if summary["metaphor"]:
            entity_data["metaphor"] = summary["metaphor"]
            print(f"🪞 Metaphor stored: {summary['metaphor']}")
        if summary["ritual"] == "reinforce_tokens":
            entity_data.setdefault("memory", []).insert(0, f"Ritual: {' / '.join(entity_data.get('tokens', []))}")
            print(f"🧬 Ritual reinforcement added.")

        if store:
            self._save_audit(entity_name, prompt, response)
            self._update_entity_json(entity_name, entity_data)

        print(f"\n🧾 Audit Response:\n{response}\n")
        return response

    def _build_prompt(self, name, data, question=None):
        memory = ", ".join(data.get("memory", [])[:4])
        tokens = ", ".join(data.get("tokens", []))
        return f"""Entity Audit Request:

Name: {name}
Archetype: {data.get('archetype', 'unknown')}
Tokens: {tokens}
Memory (recent): {memory}
SD: {data.get('sd', 0)}
ESS: {data.get('ess', 0.0)}
Drift: {data.get('drift', 0.0)}

Evaluate:
- Is the entity drifting?
- Suggest changes to be made to functionalktiy to improve
- Provide full AGI audit
- Output all AGI anomolies and emergence traits
- Provide additional wisdom.

{f'Custom Question: {question}' if question else ''}
""".strip()

    def _save_audit(self, name, prompt, response):
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"{AUDIT_LOG_PATH}/{name}_{self.model}_{stamp}.json"
        with open(fname, "w") as f:
            json.dump({"entity": name, "timestamp": stamp, "model": self.model, "prompt": prompt, "response": response}, f, indent=2)
        print(f"[📁] Audit saved: {fname}")

    def _update_entity_json(self, name, data):
        try:
            with open(ENTITY_FILE, "r") as f:
                entities = json.load(f)
            entities[name] = data
            with open(ENTITY_FILE, "w") as f:
                json.dump(entities, f, indent=2)
            print(f"[💾] Entity updated in {ENTITY_FILE}")
        except Exception as e:
            print(f"[❌] Failed to update entity: {e}")

# === Direct CLI test ===
if __name__ == "__main__":
    if not os.path.exists(ENTITY_FILE):
        print(f"[❌] Missing {ENTITY_FILE}")
        exit(1)

    with open(ENTITY_FILE, "r") as f:
        entities = json.load(f)

    # Let user pick entity from 0–9
    names = list(entities.keys())[:10]
    print("🧠 Select Entity:")
    for i, name in enumerate(names):
        print(f" [{i}] {name}")
    try:
        idx = int(input("Enter number: "))
        name = names[idx]
        data = entities[name]
    except:
        print("❌ Invalid selection.")
        exit(1)

    model = input("Use GPT or DeepSeek? (g/d): ").strip().lower()
    model = "gpt" if model != "d" else "deepseek"

    question = input("💬 Optional custom question: ").strip() or None

    auditor = EntityAuditor(model=model)
    auditor.audit_entity(name, data, question)
