# mythic_coherence.py

from difflib import SequenceMatcher

def mythic_coherence(entity) -> float:
    """
    Estimate coherence of current memory vs original motif structure.
    Proxy metric: ratio of matching symbols between snapshots.
    """

    if not hasattr(entity, "memory_snapshot") or not hasattr(entity, "current_memory"):
        return 1.0  # No comparison needed, assume full coherence

    base = entity.memory_snapshot
    current = entity.current_memory

    # Use difflib as proxy for BLEU or motif integrity score
    matcher = SequenceMatcher(None, base, current)
    return matcher.ratio()  # Value from 0.0 to 1.0
