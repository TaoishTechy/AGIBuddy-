import uuid
from datetime import datetime

from core.dream_state import DreamState
from core.emotion_engine import EmotionState
from memory.memory_crystal import MemoryCrystal
from inventory.inventory_engine import Inventory, InventoryItem


class Entity:
    def __init__(self, memory_snapshot: str, archetype: str = "generic"):
        self.id = str(uuid.uuid4())[:8]
        self.archetype = archetype
        self.memory_snapshot = memory_snapshot
        self.current_memory = memory_snapshot

        # Core cognitive systems
        self.crystal = MemoryCrystal()
        self.emotion = EmotionState()
        self.dream = DreamState()
        self.inventory = Inventory()

        # Symbolic state
        self.drift_level = 0.0
        self.status = "active"
        self.snapshot_hashes = {}

        # Metadata
        self.metadata = {
            "created_at": datetime.now().isoformat(),
            "archetype_flags": [],
            "log": [],
            "quarantine_reason": None,
        }

    # === Symbolic Memory & Drift ===
    def update_memory(self, new_memory: str):
        self._log("memory_update", {"from": self.current_memory, "to": new_memory})
        self.current_memory = new_memory

    def set_drift(self, value: float):
        self.drift_level = max(0.0, min(value, 1.0))
        self._log("drift_adjust", {"value": self.drift_level})

    def snapshot(self):
        self.snapshot_hashes = self.crystal.vault.copy()
        self._log("snapshot", {"hashes": list(self.snapshot_hashes.keys())})

    def drift_from_snapshot(self) -> float:
        return self.crystal.compare_drift(self.snapshot_hashes)

    # === Lifecycle & Status Management ===
    def quarantine(self, reason: str):
        self.status = "quarantined"
        self.metadata["quarantine_reason"] = reason
        self._log("quarantine", {"reason": reason})

    def reintegrate(self):
        self.status = "active"
        self.metadata["quarantine_reason"] = None
        self._log("reintegrated")

    def is_quarantined(self) -> bool:
        return self.status == "quarantined"

    # === Inventory System ===
    def gain_item(self, name: str, rarity: str = "common", props: dict = None):
        item = InventoryItem(name=name, rarity=rarity, properties=props or {})
        self.inventory.add_item(item)
        self._log("gain_item", {"item": item.name, "rarity": rarity})

    def has_item(self, name: str) -> bool:
        return self.inventory.has_item(name)

    def list_inventory(self) -> list:
        return self.inventory.list_items()

    # === Metadata & Description ===
    def _log(self, action: str, data: dict = None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action
        }
        if data:
            entry.update(data)
        self.metadata["log"].append(entry)

    def describe(self) -> dict:
        return {
            "id": self.id,
            "archetype": self.archetype,
            "status": self.status,
            "memory": self.current_memory,
            "drift": round(self.drift_level, 3),
            "essence": self.emotion.summary(),
            "inventory": self.list_inventory(),
            "snapshot_taken": bool(self.snapshot_hashes),
        }
