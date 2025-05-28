from flask import Blueprint, render_template_string
import random

world_bp = Blueprint("world_bp", __name__, url_prefix="/world")

@world_bp.route("/")
def world_view():
    # Simulated 10x10 symbolic tile grid
    grid_size = 10
    archetypes = ["TRUTH", "CHAOS", "HARMONY", "VOID", "LIGHT"]
    colors = {
        "TRUTH": "#00ffcc",
        "CHAOS": "#ff0066",
        "HARMONY": "#99ff00",
        "VOID": "#222222",
        "LIGHT": "#ffffff"
    }

    tiles = []
    for y in range(grid_size):
        row = []
        for x in range(grid_size):
            arc = random.choice(archetypes)
            ess = round(random.uniform(0.2, 1.2), 2)
            drift = round(random.uniform(0.1, 0.9), 2)
            row.append({
                "x": x,
                "y": y,
                "type": arc,
                "color": colors[arc],
                "ess": ess,
                "drift": drift,
                "label": f"{arc} (ess={ess}, drift={drift})"
            })
        tiles.append(row)

    return render_template_string("""
    <html>
    <head>
        <title>🌍 World Map Dashboard</title>
        <style>
            body { background:#111; color:#0f0; font-family:monospace; padding:2rem; }
            .grid { display: grid; grid-template-columns: repeat(10, 30px); gap: 1px; }
            .cell {
                width: 30px; height: 30px;
                border: 1px solid #000;
                display: inline-block;
                box-shadow: 0 0 2px #0f0;
                position: relative;
            }
            .cell:hover::after {
                content: attr(data-label);
                position: absolute;
                top: -1.5rem;
                left: 0;
                background: #000;
                color: #0f0;
                font-size: 0.75rem;
                padding: 2px 4px;
                white-space: nowrap;
                border: 1px solid #0f0;
                z-index: 10;
            }
            .legend { margin-top: 2rem; }
            .legend div { margin-bottom: 0.5rem; }
            .box {
                width: 12px; height: 12px; display: inline-block;
                margin-right: 6px; border: 1px solid #444;
            }
        </style>
    </head>
    <body>
        <h1>🌍 Symbolic World Map</h1>
        <div class="grid">
            {% for row in tiles %}
                {% for tile in row %}
                    <div class="cell"
                         style="background:{{ tile.color }};"
                         data-label="{{ tile.label }}"></div>
                {% endfor %}
            {% endfor %}
        </div>

        <div class="legend">
            <h3>🗺 Archetype Legend</h3>
            {% for arc, color in colors.items() %}
                <div><span class="box" style="background:{{ color }}"></span> {{ arc }}</div>
            {% endfor %}
        </div>

        <p>Hover over a tile to view its archetype, essence, and drift.</p>
        <a href="/">← Back</a>
    </body>
    </html>
    """, tiles=tiles, colors=colors)
