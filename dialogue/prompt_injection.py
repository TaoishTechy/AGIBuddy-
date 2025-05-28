# prompt_injection.py

from config.settings import HEALING_ECHO_RANGE

def apply_prompt_injection(entity, prompt: str) -> str:
    words = prompt.lower().split()

    # Motif injection
    if "remember" in words:
        for i, w in enumerate(words):
            if w == "remember" and i + 1 < len(words):
                motif = words[i + 1]
                entity.crystal.embed(motif)
                return f"🧠 {entity.id} now remembers '{motif}'."

    # Emotion shift
    if "feel" in words:
        for i, w in enumerate(words):
            if w == "feel" and i + 1 < len(words):
                emotion = words[i + 1]
                try:
                    entity.emotion.set(emotion, 1.25)
                    return f"💓 {entity.id} now feels heightened {emotion}."
                except:
                    return f"⚠️ Unknown emotion '{emotion}' — ignored."

    # Dream command
    if "go" in words and "silent" in words:
        entity.dream.enter("silent")
        return f"🌙 {entity.id} has entered SILENT dream layer."

    if "bloom" in words:
        entity.dream.enter("bloom")
        return f"🌸 {entity.id} has been forced into dream BLOOM."

    # Manual drift
    if "drift" in words and "up" in words:
        entity.set_drift(min(1.0, entity.drift_level + 0.2))
        return f"🌀 {entity.id}'s drift increased to {entity.drift_level:.2f}."

    if "drift" in words and "down" in words:
        entity.set_drift(max(0.0, entity.drift_level - 0.2))
        return f"🧘 {entity.id}'s drift decreased to {entity.drift_level:.2f}."

    return None  # No injection applied
