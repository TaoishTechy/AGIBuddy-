# quests/quest_engine.py

import random
import logging
from datetime import datetime
from inventory.inventory_engine import generate_item, add_item_to_inventory
from config.settings import QUEST_TYPES, QUEST_EXPERIENCE_GAIN, QUEST_FAILURE_DRIFT_PENALTY

def start_quest(entity):
    """Assign a new quest to the entity based on bias or random type."""
    if "active_quests" not in entity.metadata:
        entity.metadata["active_quests"] = []

    if len(entity.metadata["active_quests"]) >= 3:
        logging.info(f"{entity.id} already has max active quests.")
        return

    quest_type = random.choice(QUEST_TYPES)
    quest_id = f"{quest_type}_{random.randint(1000, 9999)}"
    quest = {
        "id": quest_id,
        "type": quest_type,
        "started": datetime.now().isoformat(),
        "progress": 0.0,
        "complete": False,
    }

    entity.metadata["active_quests"].append(quest)
    logging.info(f"🧭 {entity.id} accepted quest: {quest_type} (ID: {quest_id})")

def progress_quest(entity):
    """Progress the first incomplete quest and grant rewards or penalties."""
    quests = entity.metadata.get("active_quests", [])
    incomplete = [q for q in quests if not q.get("complete")]

    if not incomplete:
        start_quest(entity)
        return

    quest = incomplete[0]
    increment = round(random.uniform(0.1, 0.35), 2)
    quest["progress"] += increment

    if quest["progress"] >= 1.0:
        quest["complete"] = True
        quest["completed_at"] = datetime.now().isoformat()
        reward = generate_item(source="quest", rarity="uncommon")
        add_item_to_inventory(entity, reward)
        entity.metadata.setdefault("experience", 0)
        entity.metadata["experience"] += QUEST_EXPERIENCE_GAIN

        logging.info(f"🏁 {entity.id} completed quest {quest['id']} [{quest['type']}]")
        logging.info(f"🎁 Rewarded with {reward['name']}, +{QUEST_EXPERIENCE_GAIN} XP")

    else:
        if random.random() < 0.1:  # Simulate symbolic disruption
            drift_penalty = QUEST_FAILURE_DRIFT_PENALTY
            entity.set_drift(entity.drift_level + drift_penalty)
            logging.warning(f"⚠️ {entity.id} destabilized during quest '{quest['type']}' → Drift +{drift_penalty:.2f}")
        else:
            logging.info(f"🛠️ {entity.id} progressed on quest {quest['id']} → {quest['progress']:.2f}")
