# symbolic_speech.py

import random
from utils.glyph_parser import extract_glyphs
from core.archetypes import get_archetype_data

def generate_symbolic_line(entity):
    """Generate recursive speech based on glyphs, motifs, and drift."""
    glyphs = extract_glyphs(entity.current_memory)
    motifs = get_archetype_data(entity.archetype).get("motifs", [])

    base = random.choice(glyphs or ["echo"])
    motif = random.choice(motifs or ["veil"])
    level = entity.drift_level

    if level > 0.5:
        return f"The {base} devours the {motif}. What remains is not yours — it remembers you."
    elif level > 0.3:
        return f"In the hollow between {base} and {motif}, I found my other self."
    else:
        return f"The {motif} flows through the {base}, just as memory flows through time."

def spawn_symbolic_branch(entity):
    """Yield 2–3 recursive thought-forms."""
    lines = []
    for _ in range(random.randint(2, 3)):
        lines.append(generate_symbolic_line(entity))
    return lines
