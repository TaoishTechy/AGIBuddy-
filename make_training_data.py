# make_training_data.py
import os
import random
import string

output_dir = "training_data"
os.makedirs(output_dir, exist_ok=True)

HOLY_C_SNIPPETS = [
    '//:: RECURSIVE MYTH ENTRY',
    '#define SYMBOLIC_DENSITY 5400',
    'U0 ProcessGlyph(I64 anchor) {',
    'EchoResonance += QuantumPulse(anchor);',
    'if (anchor % 3 == 0) FusionFold();',
    '}',
    '“In the beginning, God compressed the myths into glyphs.”'
]

def generate_file(name, lines, ext=".hc"):
    with open(os.path.join(output_dir, name + ext), "w") as f:
        for _ in range(lines):
            snippet = random.choice(HOLY_C_SNIPPETS)
            filler = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=20))
            f.write(f"{snippet}  // {filler}\n")

# Generate multiple intense HolyC-style scrolls
for i in range(10):
    generate_file(f"scroll_{i}", lines=random.randint(3000, 6000), ext=".hc")

# Optional: one large symbolic TXT file
with open(os.path.join(output_dir, "mega_scroll.txt"), "w") as f:
    for _ in range(10000):
        line = random.choice(HOLY_C_SNIPPETS)
        f.write(f"{line} // Echo\n")
