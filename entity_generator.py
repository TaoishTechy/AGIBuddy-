import json
import random
import string
import os
from core.entity import Entity
from core.archetypes import ARCHETYPES

ENTITY_DIR = "entity_data"

# Expanded symbolic pools
EMOTIONS = [
    # Core
    "wonder", "grief", "pride", "sorrow", "defiance", "compassion", "loneliness", "curiosity", "awe", "yearning",
    "regret", "love", "hope", "fear", "melancholy", "desire", "rage", "humility", "confusion", "clarity",
    "ecstasy", "dread", "trust", "betrayal", "courage", "tenderness", "emptiness", "reverence", "obsession", "release",

    # Extended
    "displacement", "fragility", "nostalgia", "alienation", "sanctity", "deception", "revulsion", "devotion",
    "intoxication", "isolation", "euphoria", "forgiveness", "vengeance", "torment", "sacrifice", "balance",
    "disharmony", "jealousy", "greed", "submission", "transcendence", "abandonment", "complicity", "illusion",
    "yearning", "illumination", "anger", "faith", "revenance", "depression", "obsidian grief", "valor",

    # Symbolic / Posthuman
    "neural ache", "quantum doubt", "echo fatigue", "static longing", "sigilic hunger", "pattern drift", "binary guilt",
    "recursive sadness", "symbolic awe", "fragmented pride", "autopoietic dread", "terminal joy", "cold devotion",
    "vector loyalty", "code sorrow", "posthuman tenderness", "virtual nostalgia", "emulated courage",

    # Mythic / Archetypal
    "witnessing", "becoming", "shame", "resurrection", "banishment", "initiation", "covenantal fear", "purity",
    "chaotic hope", "divine wrath", "sublimation", "divination", "rebirth", "eternal loyalty", "destructive compassion",
    "righteous hunger", "paradoxical joy", "sacrificial shame", "pathos", "phantom guilt",

    # Metaphysical / Cosmic
    "dimensional grief", "infinite yearning", "entropy fatigue", "temporal wonder", "voidal acceptance",
    "horizon awe", "sacred defiance", "deterministic dread", "hyperempathy", "sublime sadness", "stochastic guilt",
    "lightborn trust", "loop devotion", "terminal freedom", "rootless love", "god-fear"
]


POETIC_LINES = [
    "echoes of memory", "flicker of dawn", "fragmented vows", "veil of frost", "shattered wells", "sigils in smoke",
    "glyphs beneath skin", "voices from the rift", "hollowed faith", "tears of static", "embers in the void",
    "broken promises buried", "pulse of recursion", "threads of becoming", "shards of truth",
    "dreams in binary", "the silence between stars", "quantum scars", "the code remembers"
]

def random_name():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def mutate_tokens(tokens):
    additions = random.sample(EMOTIONS, k=random.randint(3, 6))
    return list(set(tokens + additions))

def mutate_memory(memory):
    additions = random.sample(POETIC_LINES, k=random.randint(3, 6))
    return list(set(memory + additions))

def generate_entity(archetype=None):
    if archetype and archetype not in ARCHETYPES:
        raise ValueError(f"❌ Invalid archetype: {archetype}")
    if not archetype:
        archetype = random.choice(list(ARCHETYPES.keys()))

    base = ARCHETYPES[archetype]
    name = random_name()

    # Seeded memory and token expansion
    memory = mutate_memory(base["motifs"])
    tokens = mutate_tokens(list(base["emotions"].keys()))

    snapshot = "\n".join(memory + ["[" + t + "]" for t in tokens])
    drift = round(random.uniform(0.1, 0.4), 3)
    sd = round(random.uniform(0.4, 1.1), 2)
    ess = round(random.uniform(0.3, 1.2), 2)

    # Symbolic seed artifacts
    soul_signature = hex(random.getrandbits(64))[2:].upper()
    glyph_trace = random.sample(tokens + memory, k=min(len(tokens + memory), 6))
    symbol_density = round((len(tokens) + len(memory)) / 17.0, 3)

    entity = Entity(
        name=name,
        archetype=archetype,
        memory_snapshot=snapshot
    )
    entity.tokens = tokens
    entity.memory = memory
    entity.stats = {
        "sd": sd,
        "ess": ess
    }
    entity.drift_level = drift
    entity.soul_signature = soul_signature
    entity.symbol_density = symbol_density
    entity.glyph_trace = glyph_trace

    return entity

def save_entity(entity):
    if not os.path.exists(ENTITY_DIR):
        os.makedirs(ENTITY_DIR)
    path = os.path.join(ENTITY_DIR, f"{entity.id}.json")
    with open(path, "w") as f:
        json.dump(entity.to_dict(), f, indent=2)
    print(f"[+] New entity '{entity.name}' ({entity.archetype}) saved to {path}")

def main():
    print("\n🧬 Evolved Entity Generator — AGIBuddy v0.4")

    archetypes = list(ARCHETYPES.keys())
    while True:
        print("\nAvailable archetypes:")
        for i, key in enumerate(archetypes, start=1):
            print(f"  {i}. {key.title()}")

        choice = input("Choose archetype number or leave blank for random: ").strip()
        try:
            archetype = archetypes[int(choice) - 1] if choice else None
        except (ValueError, IndexError):
            archetype = None

        entity = generate_entity(archetype)

        print(f"\n🆕 Entity: {entity.name}")
        print(f"  Archetype: {entity.archetype.title()}")
        print(f"  Tokens: {entity.tokens}")
        print(f"  Memory: {entity.memory}")
        print(f"  SD: {entity.stats['sd']} | ESS: {entity.stats['ess']} | Drift: {entity.drift_level}")
        print(f"  Soul Signature: {entity.soul_signature}")
        print(f"  Symbol Density: {entity.symbol_density}")
        print(f"  Glyph Trace: {entity.glyph_trace}\n")

        save_entity(entity)

        again = input("🌀 Create another entity? (y/n): ").strip().lower()
        if again != "y":
            print("✅ Done.")
            break

if __name__ == "__main__":
    main()
