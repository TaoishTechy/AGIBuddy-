import logging
from datetime import datetime
from random import uniform, random
from math import exp

# === Thresholds & Quarantine Policy ===
DRIFT_THRESHOLD = 0.35
HOLLOW_THRESHOLD = 0.50
COHERENCE_MIN = 0.50
MAX_QUARANTINE_PER_CYCLE = 20

# === In-Memory Quarantine Tracker ===
quarantined_entities = set()

def drift_alert(entity_id, level):
    log_msg = f"[{datetime.now()}] 🚨 DRIFT ALERT: {entity_id} → {level.upper()}"
    logging.warning(log_msg)
    return {
        "event": "drift_alert",
        "entity": entity_id,
        "level": level,
        "timestamp": datetime.now().isoformat()
    }

def memory_drift(entity):
    """
    Simulate symbolic drift based on emotion state, SD, or raw uniform entropy.
    If entity has 'sd', we bias the drift upward logarithmically.
    """
    base = uniform(0.05, 0.25)
    if hasattr(entity, "sd"):
        normalized_sd = min(entity.sd / 6000, 1.5)
        return base + min(0.5, 0.3 * exp(normalized_sd - 1.0))
    return base

def mythic_coherence(entity):
    """
    Simulate symbolic coherence.
    Biases higher if ESS is high and drift is low.
    """
    base = uniform(0.3, 1.0)
    ess = getattr(entity, "ess", 0.5)
    drift = getattr(entity, "drift_level", 0.3)
    return round(min(1.0, base * (0.8 + ess) / (1.0 + drift)), 3)

def quarantine(entity, reason):
    if entity.id in quarantined_entities:
        return
    quarantined_entities.add(entity.id)
    entity.status = "quarantined"
    entity.metadata["quarantine_reason"] = reason
    entity.metadata["quarantined_at"] = datetime.now().isoformat()
    logging.info(f"🛑 Entity {entity.id} quarantined for {reason}")

def run_drift_scan(entities):
    quarantined_this_cycle = 0
    alerts = []

    for entity in entities:
        if quarantined_this_cycle >= MAX_QUARANTINE_PER_CYCLE:
            logging.warning("⚠️ Max quarantine limit reached for this cycle.")
            break

        drift = memory_drift(entity)
        coherence = mythic_coherence(entity)

        entity.set_drift(round((entity.drift_level + drift) / 2, 3))

        log_summary = (
            f"🔍 {entity.id} → Drift: {entity.drift_level:.3f} | "
            f"Coherence: {coherence:.3f} | ESS: {getattr(entity, 'ess', 0.0):.2f}"
        )
        logging.debug(log_summary)

        if drift >= DRIFT_THRESHOLD and coherence >= COHERENCE_MIN:
            quarantine(entity, "Emergent Drift")
            alerts.append(drift_alert(entity.id, "emergent"))
            quarantined_this_cycle += 1

        elif drift >= HOLLOW_THRESHOLD or coherence < COHERENCE_MIN:
            quarantine(entity, "Hollow Echo")
            alerts.append(drift_alert(entity.id, "hollow"))
            quarantined_this_cycle += 1

    return alerts
