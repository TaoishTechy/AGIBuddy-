<!DOCTYPE html>
<html>
<head>
    <title>🔍 Entity Editor</title>
    <style>
        body { background: #111; color: #ddd; font-family: monospace; padding: 2rem; }
        input, textarea, select, button { background: #222; color: #0f0; padding: 8px; border: 1px solid #444; margin: 4px; }
        .box { border: 1px solid #444; padding: 10px; margin-bottom: 1rem; background: #000; }
    </style>
</head>
<body>
<h1>🧬 Edit Entity: {{ entity["id"] }}</h1>
<form method="post">

<div class="box">
<h2>🧾 Core Attributes</h2>
<label>Archetype:</label>
<input name="archetype" value="{{ entity['archetype'] }}"><br>
<label>Status:</label>
<select name="status">
  <option value="active" {% if entity['status'] == 'active' %}selected{% endif %}>active</option>
  <option value="quarantined" {% if entity['status'] == 'quarantined' %}selected{% endif %}>quarantined</option>
</select><br>
<label>Drift:</label>
<input type="number" step="0.01" name="drift" value="{{ entity['drift'] }}"><br>
</div>

<div class="box">
<h2>🧠 Memory</h2>
<textarea name="current_memory">{{ entity['memory'][0] }}</textarea>
</div>

<div class="box">
<h2>🎒 Inventory</h2>
{% for item in entity.get("inventory", []) %}
  <div>
    {{ item["name"] }} ({{ item["rarity"] }})
    <button name="remove_item_id" value="{{ item['id'] }}">🗑️ Remove</button>
  </div>
{% endfor %}
<button name="add_item">➕ Add Random Item</button>
</div>

<button type="submit">💾 Save Changes</button>
</form>
<p><a href="/">← Back to Dashboard</a></p>
</body>
</html>
