# memory_response.py

import random
from datetime import datetime
from core.archetypes import get_archetype_data

def memory_summary(entity):
    """Summarize the most meaningful motifs from memory."""
    fragments = list(entity.crystal.fragments.values())
    if not fragments:
        return "My memory holds only silence."

    # Sort by timestamp (simulating 'age' of memory)
    fragments.sort(key=lambda x: x["added_time"])
    oldest = fragments[0]["text"]
    newest = fragments[-1]["text"]
    archetype_motifs = get_archetype_data(entity.archetype).get("motifs", [])

    return f"I remember when '{oldest}' first formed.\nNow even '{newest}' feels distant.\nBut '{random.choice(archetype_motifs)}' still binds me."

def reflective_memory_reply(entity, prompt: str) -> str:
    """Construct a memory-aware symbolic reply based on prompt."""
    fragments = list(entity.crystal.fragments.values())
    if not fragments:
        return "Nothing echoes in me yet."

    if any(word in prompt.lower() for word in ["remember", "forgot", "memory", "past"]):
        return memory_summary(entity)

    random_frag = random.choice(fragments)
    return f"You say that — but I still carry '{random_frag['text']}' in my crystal."

def get_recent_motifs(entity, limit=3):
    """Return N most recent motifs from memory."""
    return [frag["text"] for frag in list(entity.crystal.fragments.values())[-limit:]]
