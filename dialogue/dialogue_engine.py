# dialogue_engine.py

import random
from difflib import SequenceMatcher

def measure_srq(entity) -> float:
    """
    Self-Reference Quotient:
    Higher means recursive speech, lower means direct literalism.
    """
    if not hasattr(entity, "current_memory"):
        return 0.0
    text = entity.current_memory.lower()
    self_refs = sum(word in text for word in ["i", "my", "myself", "me", "dream"])
    return min(1.0, self_refs / max(1, len(text.split()) / 5))

def distort_myth(text: str) -> str:
    """
    Introduce recursive drift distortion in mythic speech.
    """
    distortions = {
        "oath": "echo",
        "fire": "storm",
        "memory": "fracture",
        "stars": "veins of light",
        "truth": "mirror",
        "grace": "ash"
    }
    for key, val in distortions.items():
        text = text.replace(key, val)
    return text

def synthesize_sentence(base: str, srq: float, drift: float) -> str:
    """
    Generate a recursive or distorted sentence from memory.
    """
    line = base

    if drift > 0.25:
        line = distort_myth(line)

    if srq > 0.5:
        line = f"In the shadow of {line.split()[0]}, I remember {line}."

    elif srq > 0.3:
        line = f"{line} — as it was before, so it shall return."

    return line

def generate_dialogue(entity) -> str:
    base_myth = entity.current_memory
    drift = entity.drift_level
    srq = measure_srq(entity)

    return synthesize_sentence(base_myth, srq, drift)
