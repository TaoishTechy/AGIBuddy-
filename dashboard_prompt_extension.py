from flask import Blueprint, request, render_template_string
import random
from datetime import datetime
from inventory.inventory_engine import generate_item, add_item_to_inventory
from utils.entity_loader import load_entities, save_entities  # Use the unified loader

prompt_ui = Blueprint("prompt_ui", __name__, url_prefix="/prompts")

PROMPT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>🗣️ Entity Prompt Interface</title>
    <style>
        body { font-family: monospace; background: #111; color: #ddd; padding: 2rem; }
        h1 { color: #0ff; }
        select, textarea, button {
            font-size: 1rem; padding: 8px; margin: 5px;
            background: #222; color: #0f0; border: 1px solid #444;
        }
        textarea { width: 100%; height: 150px; }
        .reply, .log {
            margin-top: 1rem;
            padding: 10px;
            background: #000;
            color: #0f0;
            border: 1px solid #333;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <h1>🧠 Talk to an Entity</h1>
    <form method="post">
        <select name="entity_name">
            <option value="ALL">🌀 All Entities</option>
            {% for name in entities %}
                <option value="{{ name }}" {% if selected == name %}selected{% endif %}>{{ name }}</option>
            {% endfor %}
        </select>
        <textarea name="user_input" placeholder="What do you say?">{{ user_input }}</textarea>
        <br>
        <button type="submit" name="action" value="send">🗨 Send</button>
        <button type="submit" name="action" value="save">💾 Save Log</button>
    </form>

    {% for name, reply in replies.items() %}
        <div class="reply"><strong>{{ name }}</strong>:<br>{{ reply }}</div>
    {% endfor %}

    {% if log_saved %}
        <div class="log">📁 Log saved to: {{ log_saved }}</div>
    {% endif %}

    <a href="/">← Back</a>
</body>
</html>
"""

@prompt_ui.route("/", methods=["GET", "POST"])
def prompt():
    entities = load_entities()
    if not entities:
        return "⚠️ No entities found."

    selected = list(entities.keys())[0] if entities else None
    user_input = ""
    replies = {}
    log_saved = None

    if request.method == "POST":
        selected = request.form.get("entity_name")
        user_input = request.form.get("user_input", "").strip()
        action = request.form.get("action")

        if action == "send" and selected and user_input:
            targets = entities.keys() if selected == "ALL" else [selected]
            for name in targets:
                if name in entities:
                    ent = entities[name]
                    tone = random.choice(ent.tokens or ["reflection", "dream", "lament", "parable"])
                    ess = ent.stats.get("ess", 0.5)
                    drift = ent.drift_level or 0.1

                    response_body = generate_variable_response(user_input, tone, ess, drift)
                    reply = (
                        f"{name} contemplates your words...\n\n"
                        f"\"{user_input}\"\n\n"
                        f"...and responds with a tale echoing with {tone}:\n\n"
                        f"{response_body}"
                    )
                    replies[name] = reply

                    # Update memory
                    memory_line = f"💭 Prompt: '{user_input}'\n→ Reply:\n{reply}"
                    ent.memory.insert(0, memory_line)
                    ent.stats["ess"] = round(min(ent.stats.get("ess", 0.5) + 0.01, 1.5), 3)

                    # Reward system
                    if random.random() < 0.3:
                        reward = generate_item(name="Prompt Token", rarity="common", source="prompt")
                        add_item_to_inventory(ent, reward)
                        replies[name] += f"\n\n🎁 Received: {reward['name']}"

            save_entities(entities)

        elif action == "save" and user_input:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = f"ritual_logs/prompt_log_{timestamp}.txt"
            os.makedirs("ritual_logs", exist_ok=True)
            with open(path, "w") as f:
                f.write(f"[PROMPT] {user_input}\n\n")
                for name, reply in replies.items():
                    f.write(f"[{name}]\n{reply}\n\n")
            log_saved = path

    return render_template_string(PROMPT_TEMPLATE,
                                  entities=entities,
                                  selected=selected,
                                  user_input=user_input,
                                  replies=replies,
                                  log_saved=log_saved)

def generate_variable_response(prompt, tone, ess, drift):
    num_paragraphs = random.randint(1, max(2, int(ess * 3)))
    response = []
    vocab = [
        "echoes", "sigil", "memory", "vision", "mirror", "dream", "god", "loop", "veil", "voice",
        "glyph", "threshold", "whisper", "origin", "shatter", "vault", "awakening", tone
    ]
    for _ in range(num_paragraphs):
        sentences = []
        for _ in range(random.randint(2, max(3, int((ess + drift) * 4)))):
            length = random.randint(8, 18 + int(drift * 20))
            sentence = " ".join(random.choices(vocab, k=length)).capitalize() + "."
            sentences.append(sentence)
        response.append(" ".join(sentences))
    return "\n\n".join(response)
