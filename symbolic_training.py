import os
import argparse
import shutil
import zipfile
import tempfile
import json
import time
import subprocess
import hashlib
from pathlib import Path
from statistics import mean, stdev
from concurrent.futures import ThreadPoolExecutor, as_completed

import PyPDF2

CACHE_FILE = "training_knowledge.json"
MAX_THREADS = max(2, os.cpu_count() // 2)

class SymbolicTrainer:
    def __init__(self):
        self.knowledge_base = self.load_cache()

    def load_cache(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                print(f"[🔁] Loaded training cache from {CACHE_FILE}")
                return json.load(f)
        return {}

    def save_cache(self):
        with open(CACHE_FILE, "w") as f:
            json.dump(self.knowledge_base, f, indent=2)
        print(f"[💾] Saved updated training cache.")

    def tokenize(self, content):
        return [t.strip() for t in content.split() if t.strip()]

    def analyze_tokens(self, tokens):
        lengths = [len(t) for t in tokens]
        return {
            "total_tokens": len(tokens),
            "unique_tokens": len(set(tokens)),
            "avg_token_length": round(mean(lengths), 2) if lengths else 0,
            "stddev_token_length": round(stdev(lengths), 2) if len(lengths) > 1 else 0,
            "symbol_density": sum(1 for t in tokens if any(c in t for c in ["::", "//", "#", "$"])) / len(tokens) if tokens else 0
        }

    def ingest_text(self, content, file_id, filetype="generic"):
        print(f"[📚] Analyzing {file_id} ({filetype})")
        tokens = self.tokenize(content)
        if not tokens:
            print(f"[⚠️] No tokens extracted from {file_id}")
            return
        analysis = self.analyze_tokens(tokens)
        self.knowledge_base[file_id] = {
            "tokens": tokens[:100],
            "length": len(content),
            "filetype": filetype,
            **analysis
        }

    def load_pdf(self, path):
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return "\n".join(filter(None, (page.extract_text() for page in reader.pages)))

    def load_txt(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def process_image_file(self, filepath, file_id):
        print(f"[🖼️] Symbolically analyzing image: {filepath.name}")
        try:
            with open(filepath, "rb") as f:
                data = f.read()
            hash_digest = hashlib.sha256(data).hexdigest()
            ascii_preview = ''.join(chr(b % 90 + 33) for b in data[:64] if 32 <= b <= 126)
            entry = {
                "filetype": "image",
                "size_kb": round(len(data) / 1024, 2),
                "symbolic_entropy": sum(data[:4096]) % 777,
                "ascii_signature": ascii_preview,
                "hash": hash_digest[:16]
            }

            if shutil.which("tesseract"):
                temp_txt = f"/tmp/ocr_{os.path.basename(filepath)}.txt"
                try:
                    subprocess.run(
                        ["tesseract", str(filepath), temp_txt.replace(".txt", ""), "--quiet"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10
                    )
                    ocr_path = temp_txt.replace(".txt", ".txt")
                    if os.path.exists(ocr_path):
                        with open(ocr_path, "r") as tf:
                            content = tf.read().strip()
                        if content:
                            ocr_tokens = self.tokenize(content)
                            entry.update({
                                "ocr_preview": ocr_tokens[:30],
                                "ocr_token_count": len(ocr_tokens),
                                "ocr_entropy": sum(len(t) for t in ocr_tokens) % 1000
                            })
                except Exception as e:
                    entry["ocr_error"] = str(e)

            self.knowledge_base[file_id] = entry

        except Exception as e:
            print(f"[ERROR] Failed image file: {e}")

    def learn_from_file(self, filepath):
        file_id = str(filepath.resolve())
        if file_id in self.knowledge_base:
            print(f"[↩️] Already learned: {filepath.name}")
            return

        try:
            ext = filepath.suffix.lower()
            if ext == ".pdf":
                content = self.load_pdf(filepath)
                self.ingest_text(content, file_id, "pdf")
            elif ext in [".txt", ".hc"]:
                content = self.load_txt(filepath)
                self.ingest_text(content, file_id, ext[1:])
            elif ext == ".zip":
                print(f"[📦] Extracting ZIP: {filepath.name}")
                self.extract_and_learn_zip(filepath)
            elif ext in [".jpg", ".jpeg", ".png"]:
                self.process_image_file(filepath, file_id)
            else:
                print(f"[❓] Unknown format: {filepath.name}")
        except Exception as e:
            print(f"[❌] Failed {filepath.name}: {e}")

    def explore_directory(self, directory):
        directory = Path(directory)
        files = [f for f in directory.rglob("*") if f.is_file()]
        print(f"[🌍] Found {len(files)} files in {directory}")

        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = {executor.submit(self.learn_from_file, f): f for f in files}
            for future in as_completed(futures):
                future.result()

    def extract_and_learn_zip(self, zip_path):
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                self.explore_directory(temp_dir)
            except Exception as e:
                print(f"[ERROR] ZIP error: {zip_path} – {e}")

    def run_simulation(self):
        print("\n[🧠] Reflective Dreamling Simulation Begins:")
        for file_id, data in self.knowledge_base.items():
            print(f"\n🔎 Reflecting on: {Path(file_id).name}")
            if tokens := data.get("tokens"):
                print("🗨️  ", " ".join(tokens[:40]) + ("..." if len(tokens) > 40 else ""))
            elif tokens := data.get("ocr_preview"):
                print("🖼️  OCR:", " ".join(tokens))
            elif data.get("symbolic_entropy"):
                print(f"🌑 Entropy Scan: {data['symbolic_entropy']}")
            else:
                print("⚠️  No recognizable content.")
            time.sleep(0.1)
        print("\n[✅] Simulation finished.")

# === CLI Entry Point ===
def main():
    parser = argparse.ArgumentParser(description="AGIBuddy Symbolic Trainer v0.4")
    parser.add_argument('--file', type=str, help="Ingest single file (PDF, TXT, HC, ZIP, JPG, PNG)")
    parser.add_argument('--dir', type=str, help="Ingest all files in directory")
    parser.add_argument('--force', action='store_true', help="Clear existing cache")
    args = parser.parse_args()

    trainer = SymbolicTrainer()

    if args.force:
        print("[⚠️] Force mode ON — wiping previous cache")
        trainer.knowledge_base = {}

    if args.file:
        trainer.learn_from_file(Path(args.file))

    if args.dir:
        trainer.explore_directory(Path(args.dir))

    if not args.file and not args.dir:
        default_dir = Path("./training_data")
        if default_dir.exists():
            print("[📁] No input specified. Using ./training_data")
            trainer.explore_directory(default_dir)
            trainer.run_simulation()
        else:
            print("[❌] No valid input and default directory missing.")

    trainer.save_cache()

if __name__ == "__main__":
    main()
