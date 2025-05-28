from flask import Blueprint, request, render_template_string, redirect, url_for
import os
import json
from datetime import datetime
from utils.entity_loader import load_entities

village_bp = Blueprint("village_bp", __name__, url_prefix="/village")

VILLAGE_DIR = "village_data"

PREBUILT_STRUCTURES = {
    "House": {"capacity": 3, "prosperity_boost": 0.1},
    "Market": {"capacity": 5, "prosperity_boost": 0.25},
    "Temple": {"capacity": 2, "prosperity_boost": 0.4},
    "Library": {"capacity": 4, "prosperity_boost": 0.3}
}

def load_villages():
    villages = {}
    if not os.path.exists(VILLAGE_DIR):
        os.makedirs(VILLAGE_DIR)
    for fname in os.listdir(VILLAGE_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(VILLAGE_DIR, fname), "r") as f:
                data = json.load(f)
                villages[data["name"]] = data
    return villages

def save_village(village):
    path = os.path.join(VILLAGE_DIR, f"{village['name']}.json")
    with open(path, "w") as f:
        json.dump(village, f, indent=2)

@village_bp.route("/", methods=["GET", "POST"])
def village_index():
    message = ""
    if request.method == "POST":
        new_name = request.form.get("village_name")
        if new_name:
            v = {
                "name": new_name.strip(),
                "created_at": datetime.now().isoformat(),
                "buildings": [],
                "entities": [],
                "stats": {
                    "prosperity": 1.0,
                    "population": 0
                }
            }
            save_village(v)
            message = f"✅ Created village: {new_name}"

    villages = load_villages()
    return render_template_string("""
    <html><body style="background:#111;color:#0f0;font-family:monospace;padding:2rem;">
        <h1>🏘️ Villages</h1>
        <form method="post">
            <input name="village_name" placeholder="New village name" style="background:#222;color:#0f0;">
            <button type="submit">➕ Create Village</button>
        </form>
        {% if message %}<p>{{ message }}</p>{% endif %}
        {% for name, v in villages.items() %}
            <div style="border:1px solid #0f0; padding:1rem; margin-top:1rem;">
                <strong>{{ name }}</strong> — Created: {{ v.created_at }}<br>
                Entities: {{ v.entities|length }} | Structures: {{ v.buildings|length }}<br>
                Prosperity: {{ v.stats.prosperity }} | Population: {{ v.stats.population }}<br>
                <a href="{{ url_for('village_bp.village_view', name=name) }}">🌐 View Village</a>
            </div>
        {% endfor %}
        <a href="/">← Back</a>
    </body></html>
    """, villages=villages, message=message)

@village_bp.route("/<name>", methods=["GET", "POST"])
def village_view(name):
    villages = load_villages()
    village = villages.get(name)
    if not village:
        return f"❌ Village {name} not found."

    entities = load_entities()
    msg = ""

    if request.method == "POST":
        if "assign_entity" in request.form:
            eid = request.form.get("entity_id")
            if eid and eid not in village["entities"]:
                village["entities"].append(eid)
                village["stats"]["population"] += 1
                msg = f"✅ Assigned entity {eid} to {name}"

        if "build_structure" in request.form:
            btype = request.form.get("structure_type")
            owner = request.form.get("owner_id")
            if btype in PREBUILT_STRUCTURES:
                structure = {
                    "name": btype,
                    "built_at": datetime.now().isoformat(),
                    "owner": owner or "None",
                    "capacity": PREBUILT_STRUCTURES[btype]["capacity"],
                    "prosperity_boost": PREBUILT_STRUCTURES[btype]["prosperity_boost"]
                }
                village["buildings"].append(structure)
                village["stats"]["prosperity"] += structure["prosperity_boost"]
                msg = f"🏗 Built {btype} (Owner: {owner})"

        save_village(village)

    return render_template_string("""
    <html><body style="background:#111;color:#0f0;font-family:monospace;padding:2rem;">
        <h1>🌐 Village: {{ village.name }}</h1>
        <p>Created: {{ village.created_at }}</p>
        <p>Stats → Prosperity: {{ village.stats.prosperity|round(2) }} | Population: {{ village.stats.population }}</p>

        {% if msg %}<p style="color:#0f0;">{{ msg }}</p>{% endif %}

        <h3>🧍 Assigned Entities</h3>
        <ul>
        {% for eid in village.entities %}
            <li>{{ eid }} — {{ entities[eid].name if eid in entities else 'Unknown' }}</li>
        {% endfor %}
        </ul>

        <form method="post">
            <select name="entity_id">
                {% for eid, ent in entities.items() %}
                    <option value="{{ eid }}">{{ ent.name }} ({{ eid }})</option>
                {% endfor %}
            </select>
            <button type="submit" name="assign_entity">➕ Assign to Village</button>
        </form>

        <hr>
        <h3>🏛 Build Structure</h3>
        <form method="post">
            <select name="structure_type">
                {% for s, meta in prebuilt.items() %}
                    <option value="{{ s }}">{{ s }} (Boost: {{ meta.prosperity_boost }})</option>
                {% endfor %}
            </select>
            Owner:
            <select name="owner_id">
                <option value="">None</option>
                {% for eid, ent in entities.items() %}
                    <option value="{{ eid }}">{{ ent.name }}</option>
                {% endfor %}
            </select>
            <button type="submit" name="build_structure">🏗 Build</button>
        </form>

        <h3>🏗 Built Structures</h3>
        {% for b in village.buildings %}
            <div style="margin-bottom:1rem;">
                🏠 {{ b.name }} | Owner: {{ b.owner }} | Capacity: {{ b.capacity }} | Boost: {{ b.prosperity_boost }}
                <br><small>Built: {{ b.built_at }}</small>
            </div>
        {% endfor %}

        <a href="/village">← Back to All Villages</a>
    </body></html>
    """, village=village, entities=entities, prebuilt=PREBUILT_STRUCTURES, msg=msg)
