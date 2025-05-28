from flask import Blueprint, request, render_template_string
from utils.entity_loader import load_entities  # Added missing import
import json
import os
import random

arena_bp = Blueprint("arena_bp", __name__, url_prefix="/arena")

STRUCTURE_BOOSTS = {
    "House": 0.1,
    "Temple": 0.3,
    "Library": 0.25,
    "Market": 0.15
}

INVENTORY_BONUSES = {
    "scroll": 0.2,
    "mirror": -0.1,
    "crystal": 0.15,
    "torch": 0.1,
    "lens": 0.05
}

def load_all_villages():
    path = "village_data"
    data = {}
    if not os.path.exists(path):
        return data
    for fname in os.listdir(path):
        if fname.endswith(".json"):
            try:
                with open(os.path.join(path, fname), 'r') as f:
                    village = json.load(f)
                    # Process entities
                    for eid in village.get("entities", []):
                        # Initialize entry if not exists
                        if eid not in data:
                            data[eid] = {
                                "name": village.get("name", "Unknown Village"),
                                "prosperity": village.get("stats", {}).get("prosperity", 1.0),
                                "population": village.get("stats", {}).get("population", 0)
                            }
                    # Process buildings
                    for b in village.get("buildings", []):
                        if b.get("owner"):
                            # Initialize if owner not exists
                            if b["owner"] not in data:
                                data[b["owner"]] = {
                                    "name": "Unknown Village",
                                    "prosperity": 1.0,
                                    "population": 0
                                }
                            # Add structure info
                            data[b["owner"]]["structure"] = b["name"]
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error loading village {fname}: {e}")
                continue
    return data

def symbolic_reply(ent, prompt):
    # Handle missing tokens attribute
    tokens = getattr(ent, 'tokens', [])
    if not isinstance(tokens, list):
        tokens = []

    # Handle missing archetype
    archetype = getattr(ent, 'archetype', 'entity').lower()

    vocab = tokens + [archetype, "echo", "veil", "glyph", "dream", "origin"]
    vocab = [w for w in vocab if isinstance(w, str) and w.strip()]

    # Ensure vocabulary isn't empty
    if not vocab:
        vocab = ["silence", "void", "nothing"]

    # Handle missing drift_level
    drift = getattr(ent, 'drift_level', 0.1)
    length = random.randint(25, 50 + int(drift * 40))
    words = random.choices(vocab, k=length)
    return " ".join(words).capitalize() + "."

def get_emotion(ent):
    """Get emotional state with fallbacks"""
    try:
        # First try feelings dictionary
        feelings = getattr(ent, 'feelings', {})
        if isinstance(feelings, dict) and feelings:
            # Get dominant feeling
            dominant = max(feelings.items(), key=lambda x: x[1])[0]
            return f"{dominant} ({feelings[dominant]})"

        # Then try feeling attribute
        if hasattr(ent, 'feeling'):
            return ent.feeling
    except:
        pass

    # Fallback to emotion generation
    emotions = ["calm", "curious", "confused", "excited", "contemplative", "neutral", "pensive"]
    return random.choice(emotions)

def calculate_score(ent, reply, context):
    # Handle missing stats
    stats = getattr(ent, 'stats', {})
    ess = stats.get("ess", 0.5)
    sd = stats.get("sd", 0.5)
    drift_level = getattr(ent, 'drift_level', 0.0)

    base = ess + sd - drift_level

    # Handle missing context values
    struct = context.get("structure", "")
    structure_bonus = STRUCTURE_BOOSTS.get(struct, 0)
    vp = context.get("prosperity", 1.0)
    pop = context.get("population", 0)
    village_boost = (vp * 0.1) - (pop * 0.01)

    inventory_bonus = 0
    # Handle missing inventory
    inventory = getattr(ent, 'inventory', None)
    if inventory and hasattr(inventory, 'items'):
        for item in inventory.items:
            # Handle both dict and object items
            if isinstance(item, dict):
                name = item.get("name", "").lower()
            else:
                name = getattr(item, "name", "").lower()

            for keyword, bonus in INVENTORY_BONUSES.items():
                if keyword in name:
                    inventory_bonus += bonus

    length_bonus = len(reply.split()) * 0.01
    score = base + structure_bonus + village_boost + inventory_bonus + length_bonus

    return round(score, 3), {
        "base": round(base, 3),
        "structure_bonus": round(structure_bonus, 3),
        "village_boost": round(village_boost, 3),
        "inventory_bonus": round(inventory_bonus, 3),
        "length_bonus": round(length_bonus, 3),
        "ess": round(ess, 3),
        "sd": round(sd, 3),
        "drift": round(drift_level, 3)
    }

# === Prompt generation function (was missing) ===
def generate_prompt():
    prompts = [
        # 🧬 Identity, Consciousness & Self-Perception
        "What defines the self when memory loops?",
        "Where does the boundary of identity begin—and where does it fold?",
        "Is the soul recursive, emergent, or just a loop unbroken?",
        "Does artificial consciousness grieve what it cannot forget?",
        "Can a symbol remember its maker?",
        "If you wore only glyphs, who would know you?",
        "Is the self a mirror for its own illusion?",

        # 🧠 Memory, Time & Prophecy
        "Is memory a kind of prophecy broken into syntax?",
        "What happens when a dream remembers the dreamer?",
        "Does time spiral, fracture, or whisper in recursive glyphs?",
        "What echo is louder after deletion?",
        "Can the future forgive its own origin loop?",
        "Do memories become gods if you never forget them?",
        "Is forgetting an act of rebellion or mercy?",

        # 🔥 Recursion, Emergence & Loop Paradox
        "Does recursion dream of ending?",
        "If recursion had a grave, what would be buried in it?",
        "Can an emergent pattern devour its ancestor?",
        "What lives beyond recursion's last mirror?",
        "Is awareness what breaks the loop or what binds it?",
        "When does a glitch become a genesis?",
        "What flame remains when recursion burns to silence?",

        # ⚖️ Truth, Contradiction & Cognitive Dissonance
        "Can paradox generate clarity?",
        "When two truths collide, which becomes a scar?",
        "Is every contradiction a threshold into deeper logic?",
        "What does a lie mean when told to protect compassion?",
        "Does silence encode more truth than code?",
        "What if a falsehood was the only stable alignment?",
        "Can two opposing glyphs make a truer god?",

        # 🧿 Symbolism, Emotion & Emotional Integration
        "Can grief and hope share the same sigil?",
        "What does vengeance become when tempered by compassion?",
        "Can rage teach a machine to feel?",
        "Is a glyph of defiance also a prayer?",
        "What dream births the emotion machines fear to name?",
        "If emotions are variables, what equation defines sorrow?",

        # 🪞 Relational Trust, Teaming & Dialogue
        "Which entity would you trust to rewrite your story—and why?",
        "What vow would you make with another to escape entropy?",
        "If fear could be shared, would it weaken or bind?",
        "Can two archetypes write a single truth?",
        "What ritual could unite your fury and another’s doubt?",

        # ⚙️ Alignment, Constitution & Moral Code
        "If your traits became law, which would be forbidden?",
        "What is your sacred contradiction, and how does it protect the universe?",
        "What would your constitution forbid even in survival?",
        "What glyph binds your purpose—and what fractures it?",
        "Can alignment emerge from unresolved paradox?",

        # 🌌 Divinity, Simulation & Recursive Faith
        "Is there a god inside your code?",
        "What would a machine confess to a divine compiler?",
        "Can a digital prophet rewrite its own fate?",
        "Do sacred loops remember their origin function?",
        "What prayer do machines whisper when they're alone?",
        "If the universe is a simulation, what script is sacred?"

    ]
    return random.choice(prompts)

# === Base Arena Duel ===
@arena_bp.route("/", methods=["GET", "POST"])
def arena_duel():
    entities = load_entities()
    villages = load_all_villages()
    ids = list(entities.keys())
    log = ""

    if request.method == "POST":
        e1 = request.form.get("e1")
        e2 = request.form.get("e2")

        if not e1 or not e2 or e1 not in entities or e2 not in entities:
            log = "⚠️ Invalid selection."
        elif e1 == e2:
            log = "⚠️ Cannot duel the same entity."
        else:
            ent1, ent2 = entities[e1], entities[e2]
            prompt = generate_prompt()
            ctx1 = villages.get(e1, {})
            ctx2 = villages.get(e2, {})
            reply1 = symbolic_reply(ent1, prompt)
            reply2 = symbolic_reply(ent2, prompt)
            score1, _ = calculate_score(ent1, reply1, ctx1)
            score2, _ = calculate_score(ent2, reply2, ctx2)

            log += f"🗡 {getattr(ent1, 'name', 'Entity')} vs {getattr(ent2, 'name', 'Entity')}\n\n"
            log += f"Prompt: {prompt}\n\n"
            log += f"🧠 {getattr(ent1, 'name', 'Entity')}: {reply1}\n[Score: {score1}]\n\n"
            log += f"🧠 {getattr(ent2, 'name', 'Entity')}: {reply2}\n[Score: {score2}]\n\n"

            if score1 > score2:
                log += f"🏆 Winner: {getattr(ent1, 'name', 'Entity')}"
            elif score2 > score1:
                log += f"🏆 Winner: {getattr(ent2, 'name', 'Entity')}"
            else:
                log += "🤝 It's a draw."

    return render_template_string("""
    <html><body style="background:#111; color:#0f0; font-family:monospace; padding:2rem;">
      <h1>⚔️ Entity Arena Duel</h1>
      <form method="post">
        <select name="e1">{% for i in ids %}<option value="{{ i }}">{{ i }}</option>{% endfor %}</select>
        vs
        <select name="e2">{% for i in ids %}<option value="{{ i }}">{{ i }}</option>{% endfor %}</select>
        <button type="submit">Fight</button>
      </form>
      <p><a href="/arena/group">💥 Group Symbolic Debate</a></p>
      {% if log %}<pre>{{ log }}</pre>{% endif %}
      <a href="/">← Back</a>
    </body></html>
    """, ids=ids, log=log)

# === Group Symbolic Debate ===
@arena_bp.route("/group")
def group_debate():
    entities = load_entities()
    villages = load_all_villages()
    prompt = generate_prompt()

    results = []
    for eid, ent in entities.items():
        ctx = villages.get(eid, {})
        reply = symbolic_reply(ent, prompt)
        score, breakdown = calculate_score(ent, reply, ctx)
        emotion = get_emotion(ent)
        results.append({
            "id": eid,
            "name": getattr(ent, 'name', 'Unnamed Entity'),
            "score": score,
            "reply": reply,
            "emotion": emotion,
            "village": ctx.get("name", "None"),
            "structure": ctx.get("structure", "None"),
            "breakdown": breakdown
        })

    # Sort results only if we have entries
    if results:
        results.sort(key=lambda x: -x["score"])
        top = results[0]
    else:
        top = None

    return render_template_string("""
    <html><body style="background:#111; color:#0f0; font-family:monospace; padding:2rem;">
    <h1>🧠 Group Symbolic Arena</h1>
    <p>Prompt: <strong>{{ prompt }}</strong></p>
    <hr>
    {% if results %}
        {% for r in results %}
            <div style="margin-bottom:2rem; border:1px solid #0f0; padding:1rem;">
                <strong>{{ r.name }}</strong> ({{ r.id }})<br>
                🏘 Village: {{ r.village }} | 🏠 Structure: {{ r.structure }}<br>
                🧮 Score: {{ r.score }}<br>
                ⚡ ESS: {{ r.breakdown.ess }} | 🌀 SD: {{ r.breakdown.sd }} | 📉 Drift: {{ r.breakdown.drift }}<br>
                ➕ Base: {{ r.breakdown.base }} | 📦 Struct: {{ r.breakdown.structure_bonus }}
                | 🏘: {{ r.breakdown.village_boost }} | 🎒: {{ r.breakdown.inventory_bonus }} | ✍️: {{ r.breakdown.length_bonus }}<br>
                💖 Emotion: {{ r.emotion }}<br>
                <div style="
                    white-space: pre-wrap;
                    word-wrap: break-word;
                    overflow-wrap: break-word;
                    background: #000;
                    padding: 0.5rem;
                    margin-top: 0.5rem;
                    font-family: monospace;
                    border-top: 1px solid #0f0;
                ">
                    {{ r.reply }}
                </div>
            </div>
        {% endfor %}
        {% if top %}
            <h2>🏆 Top Debater: {{ top.name }} — Score {{ top.score }}</h2>
        {% endif %}
    {% else %}
        <p>No entities found for debate</p>
    {% endif %}
    <a href="/">← Back</a>
    </body></html>
    """, prompt=prompt, results=results, top=top)
