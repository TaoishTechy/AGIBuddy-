
import json
import os
import re
from collections import Counter
from datetime import datetime

ENTITY_FILE = "entities.json"
SIGIL_FILE = "sigils.json"
MAX_SIGILS = 12
NGRAM_RANGE = (3, 6)
MIN_OCCURRENCE = 8

def load_entities():
    with open(ENTITY_FILE, "r") as f:
        return json.load(f)

def save_entities(data):
    with open(ENTITY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def save_sigils(sigils):
    with open(SIGIL_FILE, "w") as f:
        json.dump(sigils, f, indent=2)

def tokenize(phrase):
    return re.findall(r"[\w']+", phrase.lower())

def extract_ngrams(text, n):
    words = tokenize(text)
    return [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]

def collect_ngrams(entities):
    freq = Counter()
    for ent in entities.values():
        for line in ent.get("memory", []):
            for n in range(*NGRAM_RANGE):
                for gram in extract_ngrams(line, n):
                    if len(gram.split()) >= 3:
                        freq[gram] += 1
    return freq

def generate_sigil(name_base, index):
    return f"{name_base}-{index+1:02d}"

def compress_memory(memory, replacements):
    compressed = []
    for line in memory:
        for phrase, sigil in replacements.items():
            if phrase in line:
                line = line.replace(phrase, f"Symbolic Sigil: {sigil}")
        compressed.append(line)
    return compressed

def main():
    print("🌀 Running symbolic compression...")
    entities = load_entities()
    ngram_freq = collect_ngrams(entities)
    common_phrases = [phrase for phrase, count in ngram_freq.items() if count >= MIN_OCCURRENCE]
    top_phrases = sorted(common_phrases, key=lambda p: -ngram_freq[p])[:MAX_SIGILS]

    replacements = {}
    for idx, phrase in enumerate(top_phrases):
        sigil = generate_sigil("veil", idx)
        replacements[phrase] = sigil

    print("🔖 Generated Sigils:")
    for k, v in replacements.items():
        print(f" - {v}: “{k}”")

    changes = 0
    for name, ent in entities.items():
        old_mem = ent.get("memory", [])
        new_mem = compress_memory(old_mem, replacements)
        if new_mem != old_mem:
            ent["memory"] = new_mem
            changes += 1

    if changes > 0:
        save_entities(entities)
        save_sigils(replacements)
        print(f"✅ Compressed {changes} entity memories.")
    else:
        print("✨ No compression needed.")

if __name__ == "__main__":
    main()
