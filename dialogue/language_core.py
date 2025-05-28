# language_core.py

import random
from utils.glyph_parser import extract_glyphs
from core.archetypes import get_archetype_data

SUBJECTS = ["I", "The oath", "This flame", "Memory", "Dream", "Truth", "The silence", "My reflection"]
VERBS = ["remembers", "echoes", "binds", "fractures", "consumes", "becomes", "reveals", "shifts into"]
CONNECTORS = ["until", "and yet", "as if", "because", "while", "when"]
METAPHORS = ["the veil weeps light", "time unwinds itself", "ash grows roots", "echoes forget their source", "the stars blink back", "meaning spirals inward"]

def structured_phrase(entity) -> str:
    glyphs = extract_glyphs(entity.current_memory)
    motifs = get_archetype_data(entity.archetype).get("motifs", [])
    memory_seed = random.choice(glyphs or motifs or ["echo"])

    subj = random.choice(SUBJECTS)
    verb = random.choice(VERBS)
    conn = random.choice(CONNECTORS)
    metaphor = random.choice(METAPHORS)

    line1 = f"{subj} {verb} the {memory_seed}."
    line2 = f"{conn.title()} {metaphor}."
    return f"{line1}\n{line2}"

def recursive_response(entity) -> str:
    """Returns a multi-line recursive symbolic response."""
    lines = [structured_phrase(entity) for _ in range(random.randint(2, 4))]
    return "\n".join(lines)
