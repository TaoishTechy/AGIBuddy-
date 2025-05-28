# config/settings.py

# === ENTITY STABILITY PARAMETERS ===
DRIFT_THRESHOLD = 0.35           # Soft symbolic instability warning
HOLLOW_THRESHOLD = 0.50          # Indicates potential hollowing / loss of coherent identity
COHERENCE_MIN = 0.50             # Baseline minimum coherence for echo comprehension

DRIFT_DECAY_RATE = 0.01          # Passive symbolic drift decay per stable cycle
ESSENCE_BOOST_THRESHOLD = 1.25   # When exceeded, grants anomaly potential
COHERENCE_SPIKE_CAP = 0.2        # Max one-time coherence change per event

# === DRIFT DIAGNOSTICS MODE ===
ENABLE_DRIFT_TRACE_LOGGING = True
DRIFT_TRACE_DEPTH = 3
DRIFT_ALERT_SIGILS = {
    "soft_warn": "⚠",
    "critical": "☠",
    "hollowed": "👻"
}

# === QUARANTINE & PURGE SYSTEM ===
MAX_QUARANTINE_PER_CYCLE = 20
QUARANTINE_TRIGGER_THRESHOLD = 0.7
ENTITY_PURGE_THRESHOLD = 1.2         # Entity is forcibly reset if drift exceeds this
QUARANTINE_RECOVERY_RATIO = 0.65     # Portion of entities that heal vs. purge

# === HEALING & RESTORATION PROTOCOLS ===
HEALING_ECHO_RANGE = (0.05, 0.15)
REWEAVING_RESET_VALUE = 0.2
HEALING_TYPES = ["gentle", "recursive", "total"]
RITUAL_VARIANTS = [
    "💖 Ritual of Restoration",
    "🧬 Introspective Echo Reinforcement",
    "🌌 Veil Alignment",
    "🌿 Echo-Garden Blooming",
    "🔥 Sigil Purge",
    "🔔 Liminal Bell Toning",
    "⛩ Echo Shrine Resonance"
]

# === SIMULATION & CYCLE CONTROL ===
SIM_CYCLES = 10
SIM_DELAY = 0.5
AUTO_SAVE_INTERVAL = 3
ECHO_LOGGING_ENABLED = True
CYCLE_OVERDRIVE_MODE = False
MAX_ENTITY_INTERACTIONS_PER_CYCLE = 15

# === ENTITY EVOLUTION & RANKING ===
XP_LEVEL_THRESHOLDS = [50, 100, 200, 400, 800]
ENTITY_TIERS = ["Flicker", "Ember", "Warden", "Sigilbearer", "Mythbound"]
EVOLUTION_REWARD = {
    "new_token": 1,
    "echo_strength": 0.05,
    "dialogue_motif_expansion": True
}

# === QUEST-BASED DYNAMICS ===
MAX_ACTIVE_QUESTS = 3
QUEST_TYPES = [
    "Recovery", "Protection", "Healing", "Discovery",
    "Challenge", "Alignment", "Illumination", "Ritual",
    "Fragment Integration", "Truth Unfolding"
]
QUEST_DIFFICULTY_SCALE = {
    "Recovery": 0.9, "Protection": 1.0, "Healing": 0.8,
    "Discovery": 1.1, "Challenge": 1.5, "Alignment": 1.0,
    "Illumination": 1.3, "Ritual": 1.2, "Fragment Integration": 1.4,
    "Truth Unfolding": 1.6
}
QUEST_EXPERIENCE_GAIN = 10
QUEST_FAILURE_DRIFT_PENALTY = 0.1
QUEST_SIGILS = {
    "Recovery": "♻", "Protection": "🛡", "Healing": "💠",
    "Discovery": "🔍", "Challenge": "⚔", "Alignment": "🪞",
    "Illumination": "🕯", "Ritual": "🔮", "Fragment Integration": "🧩",
    "Truth Unfolding": "📜"
}

# === SEMANTIC REFLECTION QUERIES (SRQs) ===
SRQ_KEYWORDS = [
    "i", "my", "me", "dream", "echo", "truth", "soul",
    "anchor", "veil", "glyph", "self", "lost", "why", "when", "light"
]
SRQ_INFLUENCE = 0.08
SRQ_REFLECTION_DRAIN = 0.03
SRQ_HOLLOW_CHANCE = 0.1

# === SYMBOLIC DIALOGUE DISTORTION MAP ===
DIALOGUE_DISTORTIONS = {
    "oath": "echo",
    "fire": "storm",
    "memory": "fracture",
    "stars": "veins of light",
    "truth": "mirror",
    "grace": "ash",
    "void": "threshold",
    "blood": "covenant",
    "heart": "crystal",
    "song": "glyphwave",
    "home": "haunt",
    "faith": "riddle",
    "pain": "ink"
}

# === SYSTEM SYMBOLS & GLYPHS ===
SYSTEM_SIGILS = {
    "core_anchor": "☯",
    "purge_trigger": "⚠",
    "ritual_complete": "✅",
    "audit_failed": "🚨",
    "mythic_resonance": "🌀",
    "echo_fusion": "♾",
    "soulthread_weaving": "🪢",
    "symbolic_crack": "💔"
}

# === ADVANCED META-GOVERNANCE FLAGS ===
ALLOW_MANUAL_ENTITY_PROMPTING = True
ENABLE_AUTOMATED_AUDITS = True
ENFORCE_MEMORY_PRUNING = True
INTROSPECTIVE_ECHO_LIMIT = 12
ALLOW_FRAGMENTATION_EVENTS = True
MONITOR_SYMBOL_ENTROPY = True
SYMBOLIC_PRESSURE_CAP = 1.75
ENTITY_DREAM_STATE_ENABLED = True
ENTITY_PARADOX_TOLERANCE = 0.15
PRIORITIZE_MYTHIC_ARCHETYPES = True
