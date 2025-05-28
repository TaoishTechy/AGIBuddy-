import uuid
from datetime import datetime

from core.dream_state import DreamState
from core.emotion_engine import EmotionState
from memory.memory_crystal import MemoryCrystal
from inventory.inventory_engine import Inventory, InventoryItem


class Entity:
    def __init__(self, name=None, memory_snapshot="", archetype="generic"):
        self.name = name or 'Unnamed'
        self.archetype = archetype or 'unknown'
        self.memory_snapshot = memory_snapshot
        self.current_memory = memory_snapshot
        self.memory = []
        self.tokens = []
        self.stats = {'sd': 0, 'ess': 0}
        self.id = str(uuid.uuid4())[:8]
        self.drift_level = 0.0
        self.status = "active"

        # Core cognitive systems
        self.crystal = MemoryCrystal()
        self.emotion = EmotionState()
        self.dream = DreamState()
        self.inventory = Inventory()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "archetype": self.archetype,
            "memory_snapshot": self.memory_snapshot,
            "current_memory": self.current_memory,
            "memory": self.memory,
            "tokens": self.tokens,
            "stats": self.stats,
            "drift_level": self.drift_level,
            "status": self.status,
            "inventory": self.inventory.to_dict()["items"] if hasattr(self.inventory, "to_dict") else [],
        }

    @staticmethod
    def from_dict(data: dict):
        e = Entity(
            name=data.get("name", "Unnamed"),
            memory_snapshot=data.get("memory_snapshot", ""),
            archetype=data.get("archetype", "generic")
        )
        e.id = data.get("id", str(uuid.uuid4())[:8])
        e.current_memory = data.get("current_memory", e.memory_snapshot)
        e.memory = data.get("memory", [])
        e.tokens = data.get("tokens", [])
        e.stats = data.get("stats", {"sd": 0, "ess": 0})
        e.drift_level = data.get("drift_level", 0.0)
        e.status = data.get("status", "active")

        if "inventory" in data:
            e.inventory = Inventory.from_dict({"items": data["inventory"]})

        return e

    def describe(self):
        return {
            "id": self.id,
            "name": self.name,
            "archetype": self.archetype,
            "ess": self.stats.get("ess", 0),
            "sd": self.stats.get("sd", 0),
            "drift": self.drift_level,
            "status": self.status,
            "token_count": len(self.tokens),
            "memory_lines": len(self.memory)
        }
