import json
import os
import gzip
from datetime import datetime, timedelta
from pathlib import Path
from collections import OrderedDict
import logging
import psutil
from codecarbon import EmissionsTracker
from typing import Dict, List, Tuple

# Constants
ENTITY_FILE = Path("entities.json.gz")
PRUNED_LOG_DIR = Path("pruned_logs")
DASHBOARD_LOG = Path("training_data/prune_log.txt")
MAX_MEMORY_SIZE = 20  # Reduced for stability
KEEP_INTROSPECTIONS = 3  # Tighter limit
MAX_ECHO_LENGTH = 50  # Cap echo length
DRIFT_THRESHOLD = 0.65  # Stabilize high-Drift entities
MAX_CPU_PERCENT = 80  # Resource limit
PRUNE_LOG_RETENTION_DAYS = 7  # Clean old logs

# Setup
PRUNED_LOG_DIR.mkdir(exist_ok=True)
Path("training_data").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")

def load_entities() -> Dict:
    """Load entities with gzip compression."""
    try:
        if not ENTITY_FILE.exists():
            logging.warning(f"[⚠️] {ENTITY_FILE} not found, returning empty dict.")
            return {}
        with gzip.open(ENTITY_FILE, "rt", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"[❌] Failed to parse {ENTITY_FILE}: {e}")
        return {}
    except Exception as e:
        logging.error(f"[❌] Error loading entities: {e}")
        return {}

def save_entities(data: Dict) -> None:
    """Save entities with gzip compression."""
    try:
        with gzip.open(ENTITY_FILE, "wt", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logging.info(f"[💾] Entities saved to {ENTITY_FILE}")
    except Exception as e:
        logging.error(f"[❌] Error saving entities: {e}")

def prune_memory(memory: List[str], max_size: int = MAX_MEMORY_SIZE,
                 keep_intros: int = KEEP_INTROSPECTIONS,
                 max_echo_len: int = MAX_ECHO_LENGTH) -> Tuple[List[str], bool]:
    """Prune memory in a single pass with deduplication and length capping."""
    if len(memory) <= max_size:
        return memory.copy(), False

    # Single-pass categorization and deduplication
    rituals = OrderedDict()
    anchors = OrderedDict()
    intros = OrderedDict()
    sigils = OrderedDict()
    recent = memory[-10:] if len(memory) > 10 else memory[:]

    for entry in memory:
        # Truncate long entries
        entry = entry[:max_echo_len] + "..." if len(entry) > max_echo_len else entry
        # Categorize and deduplicate
        if entry.startswith("Ritual:") or entry.startswith("💖 Ritual of Restoration"):
            rituals[entry] = rituals.get(entry, 0) + 1
        elif entry.startswith("Symbolic Anchor:"):
            anchors[entry] = anchors.get(entry, 0) + 1
        elif entry.startswith("Introspective Echo:"):
            intros[entry] = intros.get(entry, 0) + 1
        elif entry.startswith("Symbolic Sigil:"):
            sigils[entry] = sigils.get(entry, 0) + 1

    # Prioritize and select entries
    selected = []
    selected.extend(list(rituals)[:max_size // 4])  # Limit rituals
    selected.extend(list(anchors)[:max_size // 4])  # Limit anchors
    selected.extend(list(intros)[:keep_intros])     # Limit introspections
    selected.extend(list(sigils)[:max_size // 8])   # Heavily limit sigils
    selected.extend([e for e in recent if e not in selected])  # Add unique recent entries

    # Ensure uniqueness and cap size
    unique = list(dict.fromkeys(selected))[-max_size + 1:]
    unique.insert(0, "🌿 Ritual of Clarity: Memories woven into harmony")
    return unique, len(unique) < len(memory)

def save_prune_log(entity_name: str, before: List[str], after: List[str]) -> None:
    """Save minimal prune logs with compression."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_entry = f"[{ts}] {entity_name} — Pruned {len(before)} → {len(after)}\n"

    # Append to dashboard log (minimal)
    with DASHBOARD_LOG.open("a") as log:
        log.write(log_entry)

    # Save detailed log (compressed)
    log_path = PRUNED_LOG_DIR / f"{entity_name}_prune_{ts}.txt.gz"
    with gzip.open(log_path, "wt", encoding="utf-8") as f:
        f.write(f"BEFORE (last 5):\n{chr(10).join(before[-5:])}\n\nAFTER (last 5):\n{chr(10).join(after[-5:])}\n")
    logging.info(f"[📜] Prune log saved: {log_path}")

def cleanup_old_logs(max_age_days: int = PRUNE_LOG_RETENTION_DAYS) -> None:
    """Delete old prune logs to save disk space."""
    cutoff = datetime.now() - timedelta(days=max_age_days)
    for log_file in PRUNED_LOG_DIR.glob("*.txt.gz"):
        if datetime.fromtimestamp(log_file.stat().st_mtime) < cutoff:
            log_file.unlink()
            logging.info(f"[🧹] Deleted old log: {log_file}")

def check_resources(max_cpu: float = MAX_CPU_PERCENT) -> bool:
    """Check system resources to prevent overload."""
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    if cpu > max_cpu or mem > max_cpu:
        logging.warning(f"[⚠️] High load: CPU {cpu:.1f}%, Mem {mem:.1f}%. Pausing...")
        return False
    return True

def main():
    """Prune entities with energy tracking and resource monitoring."""
    with EmissionsTracker(project_name="Gnostic_Dawn_Pruning") as tracker:
        if not check_resources():
            logging.info("[⏳] Waiting for resources to free up...")
            return

        entities = load_entities()
        changes = 0
        adjusted = []

        for name, ent in entities.items():
            memory = ent.get("memory", [])
            drift = ent.get("drift", 0.0)
            if not memory or (len(memory) <= MAX_MEMORY_SIZE and drift < DRIFT_THRESHOLD):
                continue

            original = memory
            pruned, was_pruned = prune_memory(original)

            if was_pruned:
                ent["memory"] = pruned
                ess_penalty = 0.02 if drift > DRIFT_THRESHOLD else 0.05
                ent["ess"] = round(max(0.1, ent.get("ess", 1.0) - ess_penalty), 2)
                ent["drift"] = round(max(0.1, drift - 0.03 if drift > DRIFT_THRESHOLD else drift), 3)
                save_prune_log(name, original, pruned)
                adjusted.append(name)
                changes += 1

        if changes > 0:
            save_entities(entities)
            cleanup_old_logs()
            logging.info(f"[✅] Pruned {changes} entities: {', '.join(adjusted)}")
        else:
            logging.info("[✨] No pruning required — all memories optimized.")

        logging.info(f"[🌍] Emissions: {tracker.final_emissions:.4f} kg CO2")

if __name__ == "__main__":
    main()
