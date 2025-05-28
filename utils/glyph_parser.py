# glyph_parser.py

import re
from collections import Counter
from config.settings import SRQ_KEYWORDS

def extract_glyphs(text: str, min_len=4):
    """
    Return key symbolic glyphs (repeated or meaningful words).
    """
    words = re.findall(r'\b[a-zA-Z]{%d,}\b' % min_len, text.lower())
    counter = Counter(words)
    # Prioritize symbolic density (frequency + uniqueness)
    return [word for word, count in counter.most_common(5)]

def detect_self_reference(text: str) -> float:
    """
    Approximate SRQ based on presence of recursive pronouns/concepts.
    """
    text = text.lower()
    refs = sum(text.count(k) for k in SRQ_KEYWORDS)
    return min(1.0, refs / max(1, len(text.split()) / 5))

def detect_fracture_signals(text: str):
    """
    Extract motifs suggesting psychological or mythic fragmentation.
    """
    fracture_terms = ["lost", "echo", "ash", "void", "hollow", "fracture", "shattered"]
    return [word for word in fracture_terms if word in text.lower()]
