import logging
from datetime import datetime
from random import uniform

from inventory.inventory_engine import generate_item  # Make sure this exists and is up to date


def healing_echo(entity):
    """
    Healing ritual: blend nostalgia + symbolic comfort to reduce drift.
    Simulated coherence improvement with symbolic placebo and reward.
    """
    if not hasattr(entity, "status") or entity.status != "reintegrated":
        return False

    pre_drift = entity.drift_level
    recovery_bonus = uniform(0.05, 0.15)

    # Simulate healing improvement
    entity.memory_snapshot = entity.current_memory
    entity.drift_level = max(0.0, pre_drift - recovery_bonus)

    # Restore to active if drift reduced sufficiently
    if entity.drift_level < 0.2:
        entity.status = "active"

    # Award healing item
    item = generate_item(name="Echo Salve", rarity="uncommon", source="healing_ritual")
    entity.gain_item(item)

    # Log healing details
    logging.info(f"[{datetime.now()}] Healing Echo on {entity.id}: Drift {pre_drift:.2f} → {entity.drift_level:.2f}, item granted: {item['name']}")
    entity.metadata.setdefault("healing_history", []).append({
        "timestamp": datetime.now().isoformat(),
        "drift_before": round(pre_drift, 3),
        "drift_after": round(entity.drift_level, 3),
        "item": item["name"]
    })

    return True


def reweaving_ritual(entity):
    """
    Deep symbolic reintegration for Hollow Echo state.
    Used when mythic coherence < 0.5 or drift > 0.5.
    """
    if not hasattr(entity, "status") or entity.status != "quarantined":
        return False

    if entity.drift_level < 0.5:
        return False  # Not at hollow threshold

    entity.memory_snapshot = entity.current_memory
    entity.drift_level = 0.2  # Residual symbolic scar
    entity.status = "reintegrated"

    # Grant deeper ritual item
    item = generate_item(name="Weave Fragment", rarity="rare", source="reweaving_ritual")
    entity.gain_item(item)

    logging.info(f"[{datetime.now()}] Reweaving Ritual for {entity.id} — reintegrated with item: {item['name']}")
    entity.metadata.setdefault("reweaving_log", []).append({
        "timestamp": datetime.now().isoformat(),
        "item": item["name"]
    })

    return True
