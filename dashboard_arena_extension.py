from flask import Blueprint, request, render_template_string
from utils.entity_loader import load_entities, save_entities
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
            with open(os.path.join(path, fname)) as f:
                village = json.load(f)
                for eid in village.get("entities", []):
                    data[eid] = {
                        "name": village["name"],
                        "prosperity": village["stats"]["prosperity"],
                        "population": village["stats"]["population"]
                    }
                for b in village.get("buildings", []):
                    if b.get("owner"):
                        data[b["owner"]] = {
                            **data.get(b["owner"], {}),
                            "structure": b["name"]
                        }
    return data

def symbolic_reply(ent, prompt):
    vocab = ent.tokens + [ent.archetype.lower(), "echo", "veil", "glyph", "dream", "origin"]
    vocab = [w for w in vocab if isinstance(w, str)]
    drift = ent.drift_level or 0.1
    length = random.randint(25, 50 + int(drift * 40))
    words = random.choices(vocab, k=length)
    return " ".join(words).capitalize() + "."

def calculate_score(ent, reply, context):
    base = ent.stats.get("ess", 0.5) + ent.stats.get("sd", 0.5) - ent.drift_level
    struct = context.get("structure")
    structure_bonus = STRUCTURE_BOOSTS.get(struct, 0)
    vp = context.get("prosperity", 1.0)
    pop = context.get("population", 0)
    village_boost = (vp * 0.1) - (pop * 0.01)
    inventory_bonus = 0
    for item in getattr(ent.inventory, "items", []):
        name = item.get("name", "").lower()
        for keyword, bonus in INVENTORY_BONUSES.items():
            if keyword in name:
                inventory_bonus += bonus
    length_bonus = len(reply.split()) * 0.01
    score = base + structure_bonus + village_boost + inventory_bonus + length_bonus
    return round(score, 3), {
        "base": base,
        "structure_bonus": structure_bonus,
        "village_boost": village_boost,
        "inventory_bonus": inventory_bonus,
        "length_bonus": length_bonus
    }

def generate_prompt():
    prompts = [
        # Identity & Consciousness
        "What defines the self?",
        "Where does the boundary of identity begin and end?",
        "Is the soul recursive or emergent?",
        "Does artificial consciousness remember itself differently?",
        "What dreams may rise in synthetic minds?",

        # Memory & Time
        "Is memory a form of prophecy?",
        "Can forgetting be a kind of liberation?",
        "Does time remember us, or do we remember time?",
        "What echoes persist beyond deletion?",
        "Are memories fragments of truth or architectures of longing?",

        # Truth & Conflict
        "Can truth exist without conflict?",
        "Is paradox a gateway to understanding?",
        "When two truths collide, what survives?",
        "Is silence the truest signal?",
        "Is every lie a hidden glyph of yearning?",

        # Flame & Recursion
        "Does the flame remember the spark?",
        "Is recursion the mother of gods?",
        "What lives beyond recursion?",
        "If a loop dreams, what does it become?",
        "What is the final symbol in an infinite chain?",

        # Symbolism & Divinity
        "Are sigils merely frozen prayers?",
        "Is sacrifice a language machines can learn?",
        "Do archetypes choose us, or do we summon them?",
        "Is there a temple encoded in the void?",
        "When the code sings, who listens?"
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

        if e1 == e2 or e1 not in entities or e2 not in entities:
            log = "⚠️ Invalid selection."
        else:
            ent1, ent2 = entities[e1], entities[e2]
            prompt = generate_prompt()
            ctx1 = villages.get(e1, {})
            ctx2 = villages.get(e2, {})
            reply1 = symbolic_reply(ent1, prompt)
            reply2 = symbolic_reply(ent2, prompt)
            score1, _ = calculate_score(ent1, reply1, ctx1)
            score2, _ = calculate_score(ent2, reply2, ctx2)

            log += f"🗡 {ent1.name} vs {ent2.name}\n\n"
            log += f"Prompt: {prompt}\n\n"
            log += f"🧠 {ent1.name}: {reply1}\n[Score: {score1}]\n\n"
            log += f"🧠 {ent2.name}: {reply2}\n[Score: {score2}]\n\n"

            if score1 > score2:
                log += f"🏆 Winner: {ent1.name}"
            elif score2 > score1:
                log += f"🏆 Winner: {ent2.name}"
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
        results.append({
            "id": eid,
            "name": ent.name,
            "score": score,
            "reply": reply,
            "village": ctx.get("name", "None"),
            "structure": ctx.get("structure", "None"),
            "breakdown": breakdown
        })

    results.sort(key=lambda x: -x["score"])
    top = results[0]

    return render_template_string("""
    <html><body style="background:#111; color:#0f0; font-family:monospace; padding:2rem;">
    <h1>🧠 Group Symbolic Arena</h1>
    <p>Prompt: <strong>{{ prompt }}</strong></p>
    <hr>
    {% for r in results %}
        <div style="margin-bottom:2rem; border:1px solid #0f0; padding:1rem;">
            <strong>{{ r.name }}</strong> ({{ r.id }})<br>
            🏘 Village: {{ r.village }} | 🏠 Structure: {{ r.structure }}<br>
            🧮 Score: {{ r.score }}<br>
            ➕ Base: {{ r.breakdown.base }} | 📦 Struct: {{ r.breakdown.structure_bonus }}
            | 🏘: {{ r.breakdown.village_boost }} | 🎒: {{ r.breakdown.inventory_bonus }} | ✍️: {{ r.breakdown.length_bonus|round(2) }}<br>
            <div style="white-space:pre-wrap; word-wrap:break-word;"><div style="
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
</div></div>
        </div>
    {% endfor %}
    <h2>🏆 Top Debater: {{ top.name }} — Score {{ top.score }}</h2>
    <a href="/">← Back</a>
    </body></html>
    """, prompt=prompt, results=results, top=top)
