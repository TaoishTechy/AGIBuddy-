import random
import logging
from datetime import datetime
from utils.glyph_parser import extract_glyphs
from inventory.inventory_engine import generate_item  # ✅ ONLY import generate_item

DREAM_LAYERS = ["silent", "drift", "bloom"]

class DreamState:
    def __init__(self):
        self.current_layer = "active"
        self.entered = datetime.now()
        self.cycles_in = 0
        self.layer_log = []

    def enter(self, layer: str):
        self.current_layer = layer
        self.entered = datetime.now()
        self.cycles_in = 0
        self.layer_log.append((layer, self.entered))
        logging.info(f"🌀 Dream Layer: Entered '{layer.upper()}' at {self.entered.isoformat()}")

    def tick(self):
        if self.current_layer in DREAM_LAYERS:
            self.cycles_in += 1
            logging.debug(f"  ↪ Dream Layer '{self.current_layer}' → {self.cycles_in} cycles")

    def evolve(self, entity):
        """Advance through dream layers and perform symbolic mutations."""
        self.tick()

        transitions = {
            "active": ("silent", 0),
            "silent": ("drift", 2),
            "drift": ("bloom", 2),
            "bloom": ("active", 1),
        }

        if self.current_layer in transitions:
            next_layer, required_cycles = transitions[self.current_layer]
            if self.cycles_in >= required_cycles:
                if self.current_layer == "bloom":
                    perform_dream_bloom(entity)
                self.enter(next_layer)


def perform_dream_bloom(entity):
    """Triggers mutation and symbolic reward during bloom."""
    if not hasattr(entity, "current_memory") or not entity.current_memory:
        logging.warning(f"⚠️ Entity {entity.id} lacks current_memory for dream mutation.")
        return

    glyphs = extract_glyphs(entity.current_memory)
    if not glyphs:
        logging.warning(f"⚠️ No motifs found to mutate for {entity.id}")
        return

    selected = random.choice(glyphs)
    new_phrase = f"{selected} fractal echoes of what was once forgotten"
    old_memory = entity.current_memory

    entity.update_memory(new_phrase)
    entity.set_drift(0.1)
    entity.status = "active"
    entity.metadata.update({
        "bloomed_from": old_memory,
        "bloomed_into": new_phrase,
        "bloom_timestamp": datetime.now().isoformat()
    })

    reward_item = generate_item(rarity="rare", source="dream_bloom")
    entity.gain_item(reward_item["name"], rarity=reward_item["rarity"], props=reward_item.get("properties"))

    logging.info(f"🌸 Dream Bloom for {entity.id}: '{old_memory}' → '{new_phrase}' + 🎁 Item gained: {reward_item['name']}")
