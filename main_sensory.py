# main_sensory.py

import os
import time
from pathlib import Path
from datetime import datetime
from sensory_hive import (
    SensoryProcessor,
    detect_usb_devices,
    print_usb_summary,
    select_device,
    print_report
)

IMAGE_DIR = Path("training_data/images")

def save_frame(frame_data, label="frame"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    target_path = IMAGE_DIR / f"{label}_{timestamp}.jpg"
    try:
        os.rename(".tmp_frame.jpg", target_path)
        return target_path
    except:
        return None

def generate_video_from_frames(output_path="output_video.mp4", fps=1):
    print(f"\n🎞️  Generating video from saved frames @ {fps} FPS...")
    try:
        os.system(f"ffmpeg -y -framerate {fps} -pattern_type glob -i '{IMAGE_DIR}/*.jpg' -c:v libx264 -pix_fmt yuv420p {output_path}")
        print(f"[✅] Video created: {output_path}")
    except Exception as e:
        print(f"[ERROR] Video creation failed: {e}")

def main():
    print("\n🧠 AGIBuddy v0.3 — Hive Vision Scan + Frame Export")
    print("===============================================================")

    sp = SensoryProcessor()
    devices = sp.get_available_devices()
    print_usb_summary()

    # === Select Video Input
    video_path = select_device("video", devices["video_devices"])
    if video_path:
        sp.enable_video(video_path)
        print(f"✅ Selected video device: {video_path}")
    else:
        print("🚫 Video test skipped.")

    # === Select Audio Input
    audio_path = select_device("audio", devices["audio_inputs"])
    if audio_path:
        sp.enable_audio(audio_path)
        print(f"✅ Selected audio device: {audio_path}")
    else:
        print("🚫 Audio test skipped.")

    # === Symbolic Vision Scan with fallback + Save frame
    captured = False
    if sp.hive["video_enabled"]:
        print("\n[🎥] Capturing from selected video device...")
        vis = sp.capture_mjpeg_frame()
        if vis["status"] == "success":
            print_report("Vision Symbol", vis, sp.hive["video_device"])
            saved = save_frame(vis, label="frame")
            if saved:
                print(f"[🖼️] Snapshot saved to: {saved}")
            captured = True
        else:
            fallback_videos = [v for v in devices["video_devices"] if v != sp.hive["video_device"]]
            for alt in fallback_videos:
                print(f"\n↩️ Retrying with alternative: {alt}")
                sp.enable_video(alt)
                vis_retry = sp.capture_mjpeg_frame()
                if vis_retry["status"] == "success":
                    print_report("Vision Symbol (Retry)", vis_retry, alt)
                    saved = save_frame(vis_retry, label="frame")
                    if saved:
                        print(f"[🖼️] Snapshot saved to: {saved}")
                    captured = True
                    break

    # === Symbolic Audio Scan — only first success reported
    if sp.hive["audio_enabled"]:
        print("\n[🎤] Listening through selected audio input...")
        aud = sp.capture_raw_audio()
        if aud["status"] == "success":
            print_report("Audio Symbol", aud, sp.hive["audio_device"])
        else:
            fallback_audio = [a for a in devices["audio_inputs"] if a != sp.hive["audio_device"]]
            for alt in fallback_audio:
                sp.enable_audio(alt)
                aud_retry = sp.capture_raw_audio()
                if aud_retry["status"] == "success":
                    print_report("Audio Symbol", aud_retry, alt)
                    break
            # Silent if all failed

    print("\n✅ Hive sensory session complete.\n")

    # === Optional: Offer to generate video
    if captured:
        choice = input("🎥 Create video from all saved frames? [y/N]: ").strip().lower()
        if choice == "y":
            try:
                fps = int(input("🕐 Enter FPS (frames per second, default 1): ").strip() or "1")
            except:
                fps = 1
            generate_video_from_frames(f"training_data/hive_output_{int(time.time())}.mp4", fps=fps)

if __name__ == "__main__":
    main()
