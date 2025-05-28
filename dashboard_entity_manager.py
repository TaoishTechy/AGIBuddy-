from flask import Blueprint, request, render_template_string, redirect, url_for
from utils.entity_loader import load_entities, save_entities
import os
import json

entity_bp = Blueprint("entity_bp", __name__, url_prefix="/entities")

ARCHETYPES = ["mystic", "warrior", "witch", "android", "merchant", "quest_giver"]
STATUSES = ["active", "dormant", "corrupted", "transcendent"]
ITEMS = [
    "Scroll of Insight", "Crystal Blade", "Mirror of Drift", "Sigil of Binding",
    "Glyph Lantern", "Token Fragment", "Lens of Seeing", "Torch of Memory",
    "Obsidian Totem", "Iron Echo"
]

def load_village_names():
    path = "village_data"
    names = []
    if os.path.exists(path):
        for fname in os.listdir(path):
            if fname.endswith(".json"):
                try:
                    with open(os.path.join(path, fname)) as f:
                        data = json.load(f)
                        names.append(data.get("name", fname.replace(".json", "")))
                except:
                    continue
    return sorted(names)

@entity_bp.route("/", methods=["GET"])
def list_entities():
    entities = load_entities()
    summaries = {eid: e.describe() for eid, e in entities.items()}
    return render_template_string("""
<html>
<body style="background:#000;color:#0f0;font-family:monospace;padding:2rem;">
  <h1>📋 Entity List</h1>
  {% for eid, ent in entities.items() %}
    <div style="margin-bottom:1rem;padding:1rem;border:1px solid #0f0;">
      <a href="{{ url_for('entity_bp.entity_detail', eid=eid) }}">
        🔍 {{ ent.name }} — {{ ent.archetype }}
      </a><br>
      ESS: {{ ent.ess }} | SD: {{ ent.sd }} | Drift: {{ ent.drift }}<br>
      Tokens: {{ ent.token_count }} | Memory Lines: {{ ent.memory_lines }}<br>
      Status: {{ ent.status }} | ID: {{ eid }}
    </div>
  {% endfor %}
  <a href="/">← Back</a>
</body>
</html>
""", entities=summaries)

@entity_bp.route("/<eid>", methods=["GET", "POST"])
def entity_detail(eid):
    entities = load_entities()
    entity = entities.get(eid)
    msg = ""

    if not entity:
        return f"❌ Entity {eid} not found."

    if request.method == "POST":
        if "delete" in request.form:
            entities.pop(eid)
            save_entities(entities)
            return redirect(url_for("entity_bp.list_entities"))

        entity.name = request.form.get("name", entity.name)
        entity.archetype = request.form.get("archetype", entity.archetype)
        entity.status = request.form.get("status", entity.status)
        entity.stats["ess"] = float(request.form.get("ess", entity.stats.get("ess", 0.5)))
        entity.stats["sd"] = float(request.form.get("sd", entity.stats.get("sd", 0.5)))
        entity.drift_level = float(request.form.get("drift", entity.drift_level))
        entity.village = request.form.get("village", entity.__dict__.get("village", "None"))

        new_item = request.form.get("new_item")
        if new_item:
            entity.inventory.add_item({"name": new_item, "rarity": "manual"})

        save_entities(entities)
        msg = "✅ Changes saved."

    villages = load_village_names()
    return render_template_string("""
    <html><body style="background:#111;color:#0f0;font-family:monospace;padding:2rem;">
        <h1>🧠 Entity Detail: {{ entity.name }}</h1>
        {% if msg %}<p style="color:#0f0;">{{ msg }}</p>{% endif %}
        <form method="post">
            <b>Name:</b> <input name="name" value="{{ entity.name }}"><br>

            <b>Archetype:</b>
            <select name="archetype">
                {% for a in archetypes %}
                    <option value="{{ a }}" {% if a == entity.archetype %}selected{% endif %}>{{ a }}</option>
                {% endfor %}
            </select><br>

            <b>Status:</b>
            <select name="status">
                {% for s in statuses %}
                    <option value="{{ s }}" {% if s == entity.status %}selected{% endif %}>{{ s }}</option>
                {% endfor %}
            </select><br>

            <b>Village:</b>
            <select name="village">
                <option value="">None</option>
                {% for v in villages %}
                    <option value="{{ v }}" {% if v == entity.__dict__.get('village') %}selected{% endif %}>{{ v }}</option>
                {% endfor %}
            </select><br>

            <hr>
            <b>ESS:</b> <input name="ess" value="{{ entity.stats['ess'] }}"><br>
            <b>SD:</b> <input name="sd" value="{{ entity.stats['sd'] }}"><br>
            <b>Drift:</b> <input name="drift" value="{{ entity.drift_level }}"><br>

            <hr>
            <b>Tokens:</b> {{ entity.tokens|join(", ") }}<br>
            <b>Inventory:</b>
            <ul>
                {% for item in entity.inventory.items %}
                    <li>{{ item.name }} ({{ item.rarity }})</li>
                {% endfor %}
            </ul>

            Add Item:
            <select name="new_item">
                <option value="">— Select —</option>
                {% for i in items %}
                    <option value="{{ i }}">{{ i }}</option>
                {% endfor %}
            </select><br>

            <hr>
            <b>Memory Snippet:</b><br>
            <textarea rows="6" cols="60" readonly>{{ entity.memory[:5]|join('\\n') }}...</textarea><br><br>

            <button type="submit">💾 Save</button>
            <button name="delete" value="1" onclick="return confirm('Delete this entity?');">🗑 Delete</button>
        </form>
        <br><a href="/entities">← Back</a>
    </body></html>
    """, entity=entity, msg=msg,
         archetypes=ARCHETYPES, statuses=STATUSES, villages=villages, items=ITEMS)
