import os

target_file = 'AGIBuddy_v0.4.3/village_dashboard.py'
full_path = f'/mnt/data/{target_file}'

# Read the existing file
with open(full_path, 'r') as file:
    lines = file.readlines()

# Look for the incorrect building restoration line and replace it
patched_lines = []
for line in lines:
    if 'village_obj.buildings = [Building.from_dict(b)' in line:
        patched_lines.append(
            '                village_obj.buildings = {b["name"]: Building.from_dict(b) for b in data.get("buildings", [])}\n'
        )
    else:
        patched_lines.append(line)

# Write the patched content back
with open(full_path, 'w') as file:
    file.writelines(patched_lines)

print("✅ Patch applied: village_dashboard.py now restores buildings as a dictionary.")
