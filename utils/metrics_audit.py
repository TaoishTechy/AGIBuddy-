# metrics_audit.py

import logging
from statistics import mean, stdev
from quests.quest_engine import entity_quests

def audit_entities(entities):
    drift_values = [e.drift_level for e in entities]
    coherent_states = [e.status for e in entities]
    quarantined = sum(1 for e in entities if e.status == "quarantined")

    drift_avg = mean(drift_values)
    drift_std = stdev(drift_values) if len(drift_values) > 1 else 0.0

    logging.info("🧠 Entity Metrics Audit")
    logging.info(f"  ↪ Total Entities       : {len(entities)}")
    logging.info(f"  ↪ Avg Drift Level     : {drift_avg:.2f}")
    logging.info(f"  ↪ Drift Variance (σ)  : {drift_std:.2f}")
    logging.info(f"  ↪ Quarantined Entities: {quarantined}")
    logging.info(f"  ↪ Status Breakdown    : {status_report(entities)}")
    print("")

def status_report(entities):
    breakdown = {}
    for e in entities:
        breakdown[e.status] = breakdown.get(e.status, 0) + 1
    return breakdown

def audit_quests():
    from quests.quest_engine import entity_quests

    if not entity_quests:
        logging.info("No active quests.")
        return

    logging.info("📜 Quest Engine Audit")
    for q in entity_quests.values():
        logging.info(f"  ↪ [{q.id}] {q.type} → {q.stages[q.current_stage]} (Active: {q.active})")
