
import os
import time
import subprocess
import json
from pathlib import Path
from datetime import datetime
from sensory_hive import SensoryProcessor

IMAGE_DIR = Path("training_data/images")
REPORT_DIR = Path("training_data/reports")
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def save_frame(label="frame"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_path = Path(".tmp_frame.jpg")
    target_path = IMAGE_DIR / f"{label}_{timestamp}.jpg"
    try:
        if temp_path.exists():
            os.rename(temp_path, target_path)
            return target_path
    except Exception as e:
        print(f"[ERROR] Could not save frame: {e}")
    return None

def run_dlib_face_detect(image_path, output_path):
    try:
        subprocess.run(["dlib_face_detect", image_path, output_path], check=True)
        return {"faces_detected": os.path.exists(output_path), "output": output_path}
    except Exception as e:
        return {"faces_detected": False, "error": str(e)}

def run_darknet_yolo(image_path, darknet_path="./darknet", config="yolov3-tiny.cfg", weights="yolov3-tiny.weights"):
    try:
        cmd = [darknet_path, "detect", config, weights, image_path, "-dont_show"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout.splitlines()
        labels = []
        for line in output:
            if "%" in line:
                label = line.split(":")[0].strip()
                confidence = line.split(":")[1].split("%")[0].strip()
                labels.append({"label": label, "confidence": confidence + "%"})
        return {"objects": labels, "raw_output": output}
    except Exception as e:
        return {"objects": [], "error": str(e)}

def analyze_snapshot(image_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    face_output = f"face_out_{timestamp}.jpg"
    face_result = run_dlib_face_detect(image_path, face_output)
    object_result = run_darknet_yolo(image_path)
    report = {
        "timestamp": timestamp,
        "input_file": str(image_path),
        "face_result": face_result,
        "object_result": object_result
    }
    report_path = REPORT_DIR / f"symbolic_scan_{timestamp}.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    return report

def loop_capture_and_analyze(cycles=5, delay=1):
    print(f"🧠 AGIBuddy v0.3 — Frame Capture Loop ({cycles}x @ {delay}s)")
    sp = SensoryProcessor()
    sp.enable_video("/dev/video0")
    for i in range(cycles):
        print(f"📷 Capturing frame {i+1}/{cycles}...")
        vis = sp.capture_mjpeg_frame()
        if vis["status"] == "success":
            saved_path = save_frame(label="loop")
            if saved_path:
                print(f"🔎 Analyzing: {saved_path}")
                result = analyze_snapshot(saved_path)
                print(json.dumps(result, indent=2))
        else:
            print(f"[ERROR] Capture failed: {vis['message']}")
        time.sleep(delay)

if __name__ == "__main__":
    loop_capture_and_analyze(cycles=5, delay=1)
