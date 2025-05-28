import os
import json
import argparse

TRAINING_CACHE = "training_knowledge.json"
NEUROCUBE_EXPORT = "neurocube.json"

def load_training_data():
    if not os.path.exists(TRAINING_CACHE):
        print(f"[⚠️] No training cache found at '{TRAINING_CACHE}'.")
        return {}

    with open(TRAINING_CACHE, "r") as f:
        return json.load(f)

def print_summary(data):
    print("\n🧠 AGIBuddy v0.3 — Training Summary Report")
    print("══════════════════════════════════════════════")

    for path, info in data.items():
        print(f"\n📄 File: {path}")
        print(f"   Type: {info.get('filetype', 'unknown')}")

        if "length" in info:
            print(f"   Tokens: {info['length']}  | Anchor Tags: {info.get('anchor_density', 0)}")
        elif "ocr_length" in info:
            print(f"   OCR Tokens: {info['ocr_token_count']} | OCR Length: {info['ocr_length']}")
        elif "symbolic_entropy" in info:
            print(f"   Entropy: {info['symbolic_entropy']} | Signature: {info.get('ascii_signature', '')[:32]}")
        else:
            print("   ⚠️ No token data found.")

def export_neurocube(knowledge_base):
    neurocube = []

    for file_id, info in knowledge_base.items():
        unit = {
            "id": file_id,
            "type": info.get("filetype", "unknown"),
            "length": info["length"],
            "anchor_density": info.get("anchor_density", 0),
            "tokens": info["tokens"][:10],  # preview of symbolic tokens
        }
        neurocube.append(unit)

    with open(NEUROCUBE_EXPORT, "w") as f:
        json.dump(neurocube, f, indent=2)

    print(f"\n🧬 NeuroCube structure exported to '{NEUROCUBE_EXPORT}'")

def main():
    parser = argparse.ArgumentParser(description="AGIBuddy Training Summary + NeuroCube Export")
    parser.add_argument('--export', action='store_true', help="Also export to neurocube.json")
    args = parser.parse_args()

    data = load_training_data()
    if not data:
        return

    print_summary(data)

    if args.export:
        export_neurocube(data)

if __name__ == "__main__":
    main()
