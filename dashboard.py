import os
import json
import random
import zipfile
from datetime import datetime
from flask import Flask, render_template_string, request

# === App Setup and Blueprints ===
from dashboard_entity_manager import entity_bp
from dashboard_arena_extension import arena_bp
from dashboard_prompt_extension import prompt_ui
from village_dashboard import village_bp
from world_map import world_bp
from utils.entity_loader import load_entities, save_entities

app = Flask(__name__)
app.register_blueprint(entity_bp, url_prefix="/entities")
app.register_blueprint(arena_bp, url_prefix="/arena")
app.register_blueprint(prompt_ui, url_prefix="/prompts")
app.register_blueprint(village_bp)
app.register_blueprint(world_bp)

# === Fallback Reader ===
def read_lines_with_fallback(path):
    encodings = ["utf-8", "latin-1", "utf-16"]
    for enc in encodings:
        try:
            with open(path, "r", encoding=enc) as f:
                return [line.strip() for line in f if line.strip()], enc
        except UnicodeDecodeError:
            continue
    return [], None

# === Symbolic Training ===
@app.route("/train")
def symbolic_training():
    entities = load_entities()
    training_logs = []
    training_path = "training_data"
    trained = 0

    def flatten_json(data):
        lines = []
        if isinstance(data, dict):
            for value in data.values():
                lines += flatten_json(value)
        elif isinstance(data, list):
            for item in data:
                lines += flatten_json(item)
        else:
            lines.append(str(data))
        return [line.strip() for line in lines if line.strip()]

    def extract_file_lines(fpath):
        ext = os.path.splitext(fpath)[1].lower()
        try:
            if ext in [".txt", ".md"]:
                return read_lines_with_fallback(fpath)
            elif ext == ".json":
                with open(fpath, "r", encoding="utf-8") as f:
                    return flatten_json(json.load(f)), "utf-8"
            elif ext == ".pdf":
                from PyPDF2 import PdfReader
                pdf = PdfReader(fpath)
                lines = []
                for page in pdf.pages:
                    content = page.extract_text()
                    if content:
                        lines.extend([line.strip() for line in content.splitlines() if line.strip()])
                return lines, "pdf"
        except Exception as e:
            return [], str(e)

        return [], None

    if not os.path.exists(training_path):
        return "⚠️ No training_data/ directory found."

    for fname in os.listdir(training_path):
        fpath = os.path.join(training_path, fname)
        ext = os.path.splitext(fname)[1].lower()

        if ext == ".zip":
            with zipfile.ZipFile(fpath, "r") as zipf:
                extract_dir = os.path.join(training_path, "_unzipped")
                zipf.extractall(extract_dir)
                for inner in os.listdir(extract_dir):
                    lines, enc = extract_file_lines(os.path.join(extract_dir, inner))
                    if lines:
                        for ent in entities.values():
                            ent.memory.extend(lines)
                            ent.stats["ess"] = round(min(ent.stats.get("ess", 0.5) + 0.01, 1.5), 3)
                        training_logs.append(f"📦 {inner} ({len(lines)} lines, {enc})")
                        trained += 1
                    else:
                        training_logs.append(f"❌ {inner}: unreadable")
        elif ext in [".txt", ".md", ".json", ".pdf"]:
            lines, enc = extract_file_lines(fpath)
            if lines:
                for ent in entities.values():
                    ent.memory.extend(lines)
                    ent.stats["ess"] = round(min(ent.stats.get("ess", 0.5) + 0.01, 1.5), 3)
                training_logs.append(f"📚 {fname} ({len(lines)} lines, {enc})")
                trained += 1
            else:
                training_logs.append(f"❌ {fname}: unreadable")

    save_entities(entities)

    return render_template_string("""
    <html>
    <head><title>🧠 Symbolic Training</title></head>
    <body style="background:#111; color:#0f0; font-family:monospace; padding:2rem;">
        <h1>🧠 Symbolic Training Complete</h1>
        {% if logs %}
            <ul>{% for line in logs %}<li>{{ line }}</li>{% endfor %}</ul>
        {% else %}
            <p>⚠️ No training files found.</p>
        {% endif %}
        <p>Trained {{ count }} entity memories.</p>
        <a href="/">← Back</a>
    </body>
    </html>
    """, logs=training_logs, count=trained)

# === Homepage ===
@app.route("/")
def index():
    return render_template_string("""
    <html><body style="background:#111; color:#0f0; font-family:monospace; padding:2rem;">
    <h1>🔥 AGIBuddy Dashboard</h1>
    <ul>
        <li><a href="/entities">📋 Entities</a></li>
        <li><a href="/arena">⚔️ Arena</a></li>
        <li><a href="/prompts">🗣️ Prompts</a></li>
        <li><a href="/village">🏘️ Village</a></li>
        <li><a href="/world">🌍 World</a></li>
        <li><a href="/train">🧠 Symbolic Training</a></li>
    </ul></body></html>
    """)

# === Error Handlers ===
@app.errorhandler(500)
def internal_error(error):
    return render_template_string(
        "<h1>🔥 Internal Server Error</h1><pre>{{ error }}</pre>", error=error
    ), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template_string("""
    <html><head><title>404 Not Found</title></head>
    <body style="background:#111;color:#fc3;font-family:monospace;padding:2rem;">
        <h1>🚫 404 - Not Found</h1>
        <pre>{{ error }}</pre>
    </body></html>
    """, error=error), 404

if __name__ == "__main__":
    app.run(debug=True)
