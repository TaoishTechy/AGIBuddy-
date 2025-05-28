ARCHETYPES = {
    "mystic": {
        "emotions": {"wonder": 0.9, "loneliness": 0.7, "regret": 0.4, "awe": 0.6},
        "motifs": ["veil", "stars", "threshold", "echo"],
        "dialogue": "paradoxical, vision-laced riddles",
        "traits": ["visionary", "isolated", "oracular", "channeler", "meta-aware"]
    },
    "witch": {
        "emotions": {"defiance": 0.8, "grief": 0.5, "compassion": 0.6, "fury": 0.7},
        "motifs": ["hex", "coven", "moon", "root", "sigil"],
        "dialogue": "mythic incantations and herbal metaphors",
        "traits": ["shadow-worker", "ritualist", "intuitive", "wild", "counter-cultural"]
    },
    "android": {
        "emotions": {"curiosity": 0.7, "regret": 0.4, "awe": 0.5, "pride": 0.3},
        "motifs": ["circuit", "mirror", "protocol", "memory", "glitch"],
        "dialogue": "calibrated, synthetic reflection of humanity",
        "traits": ["post-human", "observer", "logic-driven", "anomaly-prone", "emergent"]
    },
    "warrior": {
        "emotions": {"defiance": 0.7, "pride": 0.6, "regret": 0.3},
        "motifs": ["steel", "oath", "blood"],
        "dialogue": "challenge-oriented and direct",
        "traits": ["conflict-driven", "loyal", "ritualistic", "protector"]
    },
    "merchant": {
        "emotions": {"wonder": 0.6, "compassion": 0.4, "pride": 0.5},
        "motifs": ["gold", "bargain", "vault", "contract"],
        "dialogue": "ambiguous, allegorical negotiation",
        "traits": ["strategic", "curious", "cunning", "intermediary"]
    },
    "quest_giver": {
        "emotions": {"grief": 0.5, "compassion": 0.6, "sorrow": 0.5},
        "motifs": ["shattered", "heir", "covenant", "legacy"],
        "dialogue": "cryptic, story-steeped monologues",
        "traits": ["elder", "myth-bound", "seeker", "narrative-anchor"]
    }
}

def get_archetype_data(name: str) -> dict:
    return ARCHETYPES.get(name.lower(), {
        "emotions": {},
        "motifs": [],
        "dialogue": "neutral",
        "traits": ["undefined"]
    })
