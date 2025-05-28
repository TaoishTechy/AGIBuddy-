from collections import Counter
from utils.glyph_parser import extract_glyphs
from config.settings import SRQ_KEYWORDS
import statistics

def compute_srq(memory_text: str) -> float:
    """Calculate Self-Referential Quotient from symbolic prompt data."""
    text = memory_text.lower()
    refs = sum(text.count(k) for k in SRQ_KEYWORDS)
    return min(1.0, refs / max(1, len(text.split()) / 5))

def memory_entropy(entity) -> float:
    """Motif diversity score across memory crystal (0.0 – 1.0)."""
    motifs = [frag["text"] for frag in entity.crystal.fragments.values()]
    count = Counter(motifs)
    if not count:
        return 0.0
    diversity_ratio = len(count) / max(1, sum(count.values()))
    return round(min(diversity_ratio, 1.0), 3)

def dialogue_depth(entity) -> float:
    """Estimates symbolic depth by referencing past dialogic moments."""
    if hasattr(entity, "dialogue") and hasattr(entity.dialogue, "get_recent_responses"):
        lines = entity.dialogue.get_recent_responses(5)
    elif "dialogue_log" in entity.metadata:
        lines = entity.metadata["dialogue_log"][-5:]
    else:
        return 0.0

    reflective = sum("you said" in l.lower() or "i remember" in l.lower() or "we once" in l.lower() for l in lines)
    return round(min(reflective / 5.0, 1.0), 3)

def emotional_flux(entity) -> float:
    """Range of neurotransmitter-based emotional spread (0.0 – 1.0)."""
    levels = list(entity.emotion.levels.values())
    if not levels:
        return 0.0
    volatility = max(levels) - min(levels)
    return round(min(volatility, 1.0), 3)

def emotional_stability(entity) -> float:
    """Inverse variance across emotion neurotransmitters."""
    levels = list(entity.emotion.levels.values())
    if not levels:
        return 0.0
    variance = statistics.variance(levels) if len(levels) > 1 else 0.0
    stability = 1.0 - min(variance, 1.0)
    return round(stability, 3)

def probe_sentience(entity) -> dict:
    """
    Calculates a holistic sentience score via multiple symbolic, emotional, and reflective lenses.
    Returns tier classification and contributing metrics.
    """
    srq = compute_srq(entity.current_memory)
    entropy = memory_entropy(entity)
    dialogic = dialogue_depth(entity)
    volatility = emotional_flux(entity)
    stability = emotional_stability(entity)

    # Weighted composite model: SRQ is more impactful, stability dampens volatility
    base_score = (0.3 * srq + 0.25 * entropy + 0.25 * dialogic + 0.2 * stability)
    base_score = round(base_score, 3)

    if base_score > 0.85:
        tier = "🌀 NEXUS"
    elif base_score > 0.65:
        tier = "🌱 SEEDLING"
    elif base_score > 0.45:
        tier = "✨ SPARK"
    else:
        tier = "🕳️ SHADOW"

    return {
        "entity_id": entity.id,
        "tier": tier,
        "score": base_score,
        "metrics": {
            "SRQ": srq,
            "Memory Entropy": entropy,
            "Dialogue Depth": dialogic,
            "Emotional Flux": volatility,
            "Emotional Stability": stability
        }
    }
