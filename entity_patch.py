import os

target_file = 'AGIBuddy_v0.4.3/dashboard_entity_manager.py'
full_path = f'/mnt/data/{target_file}'

with open(full_path, 'r') as file:
    lines = file.readlines()

patched_lines = []
archetype_check_inserted = False

for line in lines:
    patched_lines.append(line)

    # Insert archetype validation near the top of manage_entities()
    if 'def manage_entities():' in line and not archetype_check_inserted:
        patched_lines.append("""
    from core.archetypes import ARCHETYPES as VALID_ARCHETYPES

    def is_valid_archetype(name):
        return name in VALID_ARCHETYPES

    def is_structure(name):
        return name.lower() in ["house", "market", "village", "bank", "arena"]

    # Patch: Intercept misrouted structure creation
    if request.method == "POST":
        archetype = request.form.get("archetype") or ""
        if is_structure(archetype):
            return f"❌ '{archetype}' is a structure, not a valid entity archetype. Use the village builder instead.", 400
        if not is_valid_archetype(archetype):
            return f"❌ Invalid archetype: '{archetype}'.", 400
""")
        archetype_check_inserted = True

# Write the patched content
with open(full_path, 'w') as file:
    file.writelines(patched_lines)

print("✅ Patch applied: Added archetype validation and blocked invalid structure creation in entity manager.")
