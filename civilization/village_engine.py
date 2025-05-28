# civilization/village_engine.py

import random
import uuid
from datetime import datetime

# Define available building types
BUILDING_TYPES = {
    "market": {"economic": 1.0},
    "bank": {"economic": 2.0},
    "barracks": {"security": 1.5},
    "training_camp": {"education": 1.2},
    "university": {"education": 2.0},
    "arena": {"culture": 1.0},
    "blacksmith": {"craft": 1.5},
    "tavern": {"morale": 1.0},
    "library": {"knowledge": 1.5},
}

class Building:
    def __init__(self, name, level=1):
        self.name = name
        self.level = level
        self.health = 100
        self.upgrade_cost = 100 * level

    def upgrade(self):
        self.level += 1
        self.health = 100
        self.upgrade_cost = 100 * self.level

    def to_dict(self):
        return {
            "name": self.name,
            "level": self.level,
            "health": self.health,
            "upgrade_cost": self.upgrade_cost,
        }

    @staticmethod
    def from_dict(data):
        return Building(
            name=data.get("name"),
            level=data.get("level", 1)
        )


class Village:
    def __init__(self, name, id=None, population=0, buildings=None, owner=None, visit_log=None, drift=0.0):
        self.id = id or str(uuid.uuid4())[:8]
        self.name = name
        self.population = population
        self.drift = drift
        self.owner = owner
        self.visit_log = visit_log or []

        # Ensure buildings is always a dictionary
        if isinstance(buildings, dict):
            self.buildings = {
                k: (v if isinstance(v, Building) else Building.from_dict(v))
                for k, v in buildings.items()
            }
        else:
            self.buildings = {}

    def log(self, message):
        timestamp = datetime.now().isoformat()
        self.visit_log.append(f"[{timestamp}] {message}")

    def add_building(self, name):
        if name not in BUILDING_TYPES:
            return False
        if name in self.buildings:
            return False  # Already exists
        self.buildings[name] = Building(name)
        self.log(f"🏗️ Constructed {name}")
        return True

    def upgrade_building(self, name):
        if name in self.buildings:
            self.buildings[name].upgrade()
            self.log(f"⬆️ Upgraded {name} to level {self.buildings[name].level}")
            return True
        return False

    def tick(self):
        """Simulate one passage of time in the village."""
        # Simulate drift and morale fluctuation
        old_drift = self.drift
        self.drift = max(0.0, self.drift + random.uniform(-0.01, 0.03))
        if self.drift > 0.5 and random.random() < 0.2:
            self.log("⚠️ Village drift is high — strange tensions emerge.")

        # Random building damage (simulated wear)
        for b in self.buildings.values():
            b.health = max(0, b.health - random.randint(0, 2))
        self.log(f"🔁 Drift tick: {round(old_drift, 3)} → {round(self.drift, 3)}")

    def summary(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "owner": self.owner,
            "drift": round(self.drift, 3),
            "building_count": len(self.buildings),
        }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "owner": self.owner,
            "drift": self.drift,
            "visit_log": self.visit_log,
            "buildings": {k: b.to_dict() for k, b in self.buildings.items()},
        }

    @staticmethod
    def from_dict(data):
        return Village(
            name=data.get("name"),
            id=data.get("id"),
            population=data.get("population", 0),
            buildings=data.get("buildings", {}),
            owner=data.get("owner"),
            visit_log=data.get("visit_log", []),
            drift=data.get("drift", 0.0),
        )
