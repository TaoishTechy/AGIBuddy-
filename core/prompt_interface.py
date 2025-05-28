import random
import html
from dialogue.symbolic_speech import spawn_symbolic_branch
from dialogue.dialogue_engine import generate_dialogue


def sanitize_text(text: str) -> str:
    """
    Escape HTML-sensitive characters and preserve line breaks for HTML rendering.
    """
    return html.escape(text).replace("\n", "<br>")


def query_entity(entity, prompt: str) -> str:
    """
    Accepts a multiline prompt and returns a symbolic or memory-reactive response.
    Supports drift-based symbolic speech or mythic logic reflection.
    """
    # Apply emotional mutation based on symbolic drift
    entity.emotion.mutate(drift_factor=entity.drift_level)

    # Symbolic Fragment Mode
    if entity.drift_level > 0.5:
        fragments = spawn_symbolic_branch(entity)
        reply = "\n".join(fragments)

    # Mythopoetic Reflection
    elif "?" in prompt or "why" in prompt.lower():
        reply = generate_dialogue(entity)

    # Default Recall
    else:
        reply = f"{entity.id} says:\n{entity.current_memory}"

    # Store memory exchange formatted for future processing/logging
    formatted_prompt = prompt.strip().replace("\r", "")
    formatted_reply = reply.strip().replace("\r", "")
    memory_entry = f"💭 Prompt:\n{formatted_prompt}\n→ Reply:\n{formatted_reply}"

    entity.current_memory = formatted_reply  # Update core memory trace
    entity.metadata.setdefault("dialogue_log", []).append(memory_entry)

    return reply
