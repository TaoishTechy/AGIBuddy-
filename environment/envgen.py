import random
from datetime import datetime

# === Symbolic Area Definitions ===
AREA_ARCHETYPES = {
    "tavern": {
        "motifs": ["golden ale", "whispers", "old songs"],
        "boost": {"serotonin": 0.05},
        "quest_bias": ["Recovery", "Discovery"]
    },
    "battlefield": {
        "motifs": ["shattered oaths", "blood", "drift of fallen dreams"],
        "boost": {"drift": 0.1},
        "quest_bias": ["Healing", "Challenge"]
    },
    "sanctuary": {
        "motifs": ["breathwoven well", "grace echoes", "silent stones"],
        "boost": {"serotonin": 0.1, "drift": -0.05},
        "quest_bias": ["Healing", "Discovery"]
    },
    "ruins": {
        "motifs": ["fractured thrones", "ashes", "forgotten wells"],
        "boost": {"loneliness": 0.1, "wonder": 0.1},
        "quest_bias": ["Discovery", "Myth Reintegration"]
    },
    "lorehouse": {
        "motifs": ["glyphwave", "echo scrolls", "veins of memory"],
        "boost": {"dopamine": 0.05},
        "quest_bias": ["Illumination", "Discovery"]
    },
    "obsidian shrine": {
        "motifs": ["void chant", "mirror glyph", "soul ash"],
        "boost": {"oxytocin": -0.05, "serotonin": 0.03},
        "quest_bias": ["Challenge", "Alignment"]
    }
}

# === Classes ===

class SymbolicArea:
    def __init__(self, area_type=None):
        self.type = area_type or random.choice(list(AREA_ARCHETYPES.keys()))
        self.creation_time = datetime.now()
        self.motifs = AREA_ARCHETYPES[self.type]["motifs"]
        self.effects = AREA_ARCHETYPES[self.type]["boost"]
        self.quest_bias = AREA_ARCHETYPES[self.type]["quest_bias"]
        self.visits = 0
        self.drift = 0.0

    def reinforce(self):
        self.visits += 1
        self.drift = max(0.0, self.drift - 0.03)

    def decay(self, external_drift=0.0):
        drift_gain = 0.01 + external_drift * 0.05
        self.drift += drift_gain
        if self.drift > 0.5 and random.random() < 0.3:
            self.mutate()

    def mutate(self):
        old_type = self.type
        self.type = random.choice(list(AREA_ARCHETYPES.keys()))
        archetype = AREA_ARCHETYPES[self.type]
        self.motifs = archetype["motifs"]
        self.effects = archetype["boost"]
        self.quest_bias = archetype["quest_bias"]
        self.drift = 0.2
        print(f"⚠️ Area mutated from {old_type} → {self.type}")

    def summary(self):
        return {
            "type": self.type,
            "motifs": self.motifs,
            "drift": round(self.drift, 2),
            "visits": self.visits,
            "quest_bias": self.quest_bias
        }

class Town:
    def __init__(self, name):
        self.name = name
        self.areas = [SymbolicArea() for _ in range(random.randint(3, 6))]
        self.foundation = datetime.now()
        self.culture_bias = random.choice(["fire", "veil", "mirror", "storm", "glyph"])

    def evolve(self):
        for area in self.areas:
            area.decay(external_drift=random.uniform(0.01, 0.05))

    def summary(self):
        return {
            "town": self.name,
            "culture": self.culture_bias,
            "areas": [a.summary() for a in self.areas]
        }

class Nation:
    def __init__(self, name, num_towns=3):
        self.name = name
        self.creation_time = datetime.now()
        self.towns = [Town(f"{name}-Town-{i+1}") for i in range(num_towns)]
        self.ideological_drift = random.uniform(0.1, 0.4)
        self.symbolic_trait = random.choice(["dream", "grief", "pride", "light", "threshold"])

    def simulate_cycle(self):
        for town in self.towns:
            town.evolve()

    def summary(self):
        return {
            "nation": self.name,
            "trait": self.symbolic_trait,
            "drift": round(self.ideological_drift, 3),
            "towns": [t.summary() for t in self.towns]
        }

# === Demo Entry Point ===

if __name__ == "__main__":
    realm = Nation("Mythara", num_towns=4)
    realm.simulate_cycle()

    import json
    print(json.dumps(realm.summary(), indent=2))
