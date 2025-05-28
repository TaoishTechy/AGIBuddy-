# memory_drift.py

import hashlib

def hash_memory(memory_blob: str) -> str:
    """Generate SHA-256 hash of a memory string."""
    return hashlib.sha256(memory_blob.encode('utf-8')).hexdigest()

def calculate_hash_delta(hash1: str, hash2: str) -> float:
    """Return percent difference between two SHA-256 hashes."""
    diffs = sum(c1 != c2 for c1, c2 in zip(hash1, hash2))
    return diffs / len(hash1)  # Normalize to 0–1 float

def memory_drift(entity) -> float:
    """
    Calculates memory drift for an entity based on previous and current memory snapshots.
    You must provide entity.memory_snapshot and entity.current_memory.
    """
    if not hasattr(entity, "memory_snapshot") or not hasattr(entity, "current_memory"):
        return 0.0  # No memory to compare, assume no drift yet

    h1 = hash_memory(entity.memory_snapshot)
    h2 = hash_memory(entity.current_memory)
    return calculate_hash_delta(h1, h2)
