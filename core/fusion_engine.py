import logging
from core.entity import Entity
from collections import defaultdict
from itertools import combinations
from datetime import datetime

FUSION_DRIFT_THRESHOLD = 0.2
FUSION_COHERENCE_MIN = 0.85
MIN_SHARED_GLYPHS = 2
MAX_FUSIONS_PER_CYCLE = 5  # throttle excessive chaining

def extract_glyphs_from_crystal(crystal):
    return set(fragment["text"] for fragment in crystal.fragments.values())

def find_fusion_pairs(entities):
    candidates = []
    for e1, e2 in combinations(entities, 2):
        if e1.status != "active" or e2.status != "active":
            continue
        if e1.drift_level > FUSION_DRIFT_THRESHOLD or e2.drift_level > FUSION_DRIFT_THRESHOLD:
            continue

        glyphs1 = extract_glyphs_from_crystal(e1.crystal)
        glyphs2 = extract_glyphs_from_crystal(e2.crystal)
        shared = glyphs1 & glyphs2

        if len(shared) >= MIN_SHARED_GLYPHS:
            coherence = compute_coherence(glyphs1, glyphs2)
            if coherence >= FUSION_COHERENCE_MIN:
                candidates.append((e1, e2, shared, coherence))
    return sorted(candidates, key=lambda x: -x[3])  # sort by highest coherence

def compute_coherence(set1, set2):
    if not set1 or not set2:
        return 0.0
    union = set1 | set2
    intersection = set1 & set2
    return len(intersection) / len(union)

def fuse_entities(e1, e2, shared_motifs):
    if not isinstance(entity_a, dict) or not isinstance(entity_b, dict):
        raise TypeError('Entities must be dictionaries to fuse')
    # Simple fusion strategy: A takes priority, B fills gaps
    fused = entity_a.copy()
    for k, v in entity_b.items():
        if k not in fused or fused[k] in [None, '', []]:
            fused[k] = v
    return fused
    merged_memory = f"{e1.current_memory} + {e2.current_memory}"
    merged_entity = Entity(memory_snapshot=merged_memory, archetype="mythic_nexus")

    for frag in e1.crystal.fragments.values():
        merged_entity.crystal.embed(frag["text"])
    for frag in e2.crystal.fragments.values():
        merged_entity.crystal.embed(frag["text"])

    merged_entity.metadata["fused_from"] = [e1.id, e2.id]
    merged_entity.metadata["shared_motifs"] = list(shared_motifs)
    merged_entity.metadata["fusion_time"] = datetime.now().isoformat()
    merged_entity.status = "active"
    merged_entity.set_drift((e1.drift_level + e2.drift_level) / 2)
    merged_entity.metadata["fusion_score"] = compute_coherence(
        extract_glyphs_from_crystal(e1.crystal), extract_glyphs_from_crystal(e2.crystal))

    logging.info(f"⚡ Fusion Event: {e1.id} + {e2.id} → {merged_entity.id} with {len(shared_motifs)} shared motifs")

def run_fusion_cycle(entities):
    fusions = []
    fusion_pairs = find_fusion_pairs(entities)
    already_fused_ids = set()

    for e1, e2, shared, _ in fusion_pairs:
        if e1.id in already_fused_ids or e2.id in already_fused_ids:
            continue
        fused = fuse_entities(e1, e2, shared)
        fusions.append(fused)
        already_fused_ids.update([e1.id, e2.id])

        if len(fusions) >= MAX_FUSIONS_PER_CYCLE:
            break
