import random

NEUROCHEMICALS = [
    "serotonin",      # mood, well-being
    "oxytocin",       # bonding, trust
    "dopamine",       # reward, motivation
    "endorphin",      # pleasure, pain relief
    "norepinephrine", # alertness, arousal
    "acetylcholine",  # attention, learning
    "glutamate",      # excitation, memory
    "GABA",           # inhibition, calm
    "vasopressin",    # territoriality, aggression
    "cortisol"        # stress, vigilance
]

# Baseline operating levels (0.0–1.5)
DEFAULT_LEVELS = {
    "serotonin": 1.0,
    "oxytocin": 1.0,
    "dopamine": 1.0,
    "endorphin": 1.0,
    "norepinephrine": 1.0,
    "acetylcholine": 1.0,
    "glutamate": 1.0,
    "GABA": 1.0,
    "vasopressin": 1.0,
    "cortisol": 0.5  # typically lower when relaxed
}

class EmotionState:
    def __init__(self):
        self.levels = DEFAULT_LEVELS.copy()

    def mutate(self, drift_factor: float = 0.0):
        """Apply nuanced modulation per neurotransmitter influenced by drift."""
        for key in self.levels:
            # Random fluctuation
            fluctuation = random.uniform(-0.05, 0.05)
            # Custom drift sensitivities
            drift_influence = {
                "serotonin": -0.02 * drift_factor,
                "dopamine":  0.015 * drift_factor,
                "cortisol":  0.025 * drift_factor,
                "GABA":     -0.015 * drift_factor,
                "glutamate": 0.02 * drift_factor
            }.get(key, 0.0)

            # Update level within bounded range
            new_value = self.levels[key] + fluctuation + drift_influence
            self.levels[key] = max(0.0, min(1.5, new_value))

    def set(self, key, value):
        if key in self.levels:
            self.levels[key] = max(0.0, min(1.5, value))

    def get(self, key):
        return self.levels.get(key, 0.0)

    def summary(self):
        return {k: round(v, 2) for k, v in self.levels.items()}
