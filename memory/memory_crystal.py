# memory_crystal.py

import hashlib
from datetime import datetime

class MemoryCrystal:
    def __init__(self):
        self.fragments = {}  # key: hash, value: {text, added_time}
        self.vault = []      # historical motif hashes
        self.rewrite_log = []

    def hash_motif(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def embed(self, motif_text: str) -> str:
        h = self.hash_motif(motif_text)
        if h not in self.fragments:
            self.fragments[h] = {
                "text": motif_text,
                "added_time": datetime.now().isoformat()
            }
            self.vault.append(h)
        return h

    def retrieve(self, h: str) -> str:
        return self.fragments.get(h, {}).get("text", "")

    def rewrite_fragment(self, old_hash: str, new_text: str):
        if old_hash in self.fragments:
            self.rewrite_log.append({
                "old_hash": old_hash,
                "old_text": self.fragments[old_hash]["text"],
                "new_text": new_text,
                "timestamp": datetime.now().isoformat()
            })
            del self.fragments[old_hash]
        return self.embed(new_text)

    def compare_drift(self, snapshot: list) -> float:
        """Compare current vault vs. a snapshot of hashes."""
        if not snapshot:
            return 0.0
        differences = sum(1 for h in snapshot if h not in self.vault)
        return differences / len(snapshot)
