# lore_engine.py

from datetime import datetime
from utils.glyph_parser import extract_glyphs

def generate_lore_scroll(entity) -> str:
    name = entity.id
    archetype = entity.archetype
    motifs = [frag["text"] for frag in entity.crystal.fragments.values()]
    recent_prompts = entity.dialogue.get_recent_prompts(3) if hasattr(entity, "dialogue") else []
    fusion_from = entity.metadata.get("fused_from", [])
    dream_state = entity.dream.current_layer if hasattr(entity, "dream") else "unknown"

    scroll = []

    # 📜 Title
    name = str(entity.id) if hasattr(entity, "id") else "UNKNOWN"
    scroll.append(f"╔═══════════ LORE SCROLL: {name.upper()} ═══════════╗\n")
    scroll.append(f"↳ Archetype: {archetype}")
    scroll.append(f"↳ Dream Layer: {dream_state.upper()}")
    if fusion_from:
        scroll.append(f"↳ Fused from: {', '.join(fusion_from)}")

    scroll.append("")

    # 🧠 Memory Motifs
    scroll.append("◆ MEMORY CRYSTAL MOTIFS:")
    if not motifs:
        scroll.append("   • The crystal sleeps...")
    else:
        for m in motifs[-5:]:
            scroll.append(f"   • {m}")

    scroll.append("")

    # 💬 Dialogue Echoes
    scroll.append("◆ DIALOGUE ECHOES:")
    if not recent_prompts:
        scroll.append("   • No echoes recorded.")
    else:
        for p in recent_prompts:
            scroll.append(f"   • \"{p}\"")

    scroll.append("")

    # 🌀 Symbolic Reflection
    if motifs:
        core = motifs[-1]
        scroll.append("◆ SYMBOLIC RECURSION:")
        scroll.append(f"   • \"In the end, all things returned to {core}.\"")

    scroll.append("\n╚════════════════════════════════════════════════════╝")

    return "\n".join(scroll)
