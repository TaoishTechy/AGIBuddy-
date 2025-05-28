import os
import threading

class SensoryProcessor:
    def __init__(self):
        self.video_devices = self._find_video_devices()
        self.audio_inputs = self._find_audio_inputs()
        self.hive = {
            "video_enabled": False,
            "audio_enabled": False,
            "video_device": None,
            "audio_device": None
        }

    def _find_video_devices(self):
        return [f"/dev/video{i}" for i in range(10) if os.path.exists(f"/dev/video{i}")]

    def _find_audio_inputs(self):
        inputs = []
        for root, dirs, files in os.walk("/dev/snd"):
            for f in files:
                if "pcm" in f and "c" in f:
                    inputs.append(os.path.join(root, f))
        return inputs

    def enable_video(self, device):
        if device in self.video_devices:
            self.hive["video_device"] = device
            self.hive["video_enabled"] = True
            return True
        return False

    def enable_audio(self, device):
        if device in self.audio_inputs:
            self.hive["audio_device"] = device
            self.hive["audio_enabled"] = True
            return True
        return False

    def capture_mjpeg_frame(self, out_file=".tmp_frame.jpg", width=640, height=480):
        dev = self.hive["video_device"]
        if not self.hive["video_enabled"] or not dev:
            return {"status": "error", "message": "Video capture disabled or unassigned."}

        try:
            result = os.system(
                f"v4l2-ctl --device={dev} --set-fmt-video=width={width},height={height},pixelformat=MJPG "
                f"--stream-mmap=3 --stream-count=1 --stream-to={out_file} > /dev/null 2>&1"
            )
            if not os.path.exists(out_file) or os.path.getsize(out_file) < 1000:
                return {"status": "error", "message": "Failed to retrieve JPEG via v4l2-ctl."}

            with open(out_file, "rb") as f:
                data = f.read()
            start = data.find(b'\xff\xd8')
            end = data.find(b'\xff\xd9', start)
            jpeg_data = data[start:end+2] if start >= 0 and end > start else data[:1024]
            entropy = sum(jpeg_data[:300]) % 777 if jpeg_data else 0
            return {
                "file": out_file,
                "size_kb": round(len(jpeg_data) / 1024, 1),
                "symbolic_entropy": entropy,
                "jpeg_header": list(jpeg_data[:16]),
                "status": "success"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def capture_raw_audio(self, bytes_to_read=4096, timeout_sec=2):
        dev = self.hive["audio_device"]
        if not self.hive["audio_enabled"] or not dev:
            return {"status": "error", "message": "Audio capture disabled or unassigned."}

        def try_read():
            try:
                with open(dev, "rb") as f:
                    self.audio_bytes = f.read(bytes_to_read)
            except:
                self.audio_bytes = b""

        self.audio_bytes = b""
        thread = threading.Thread(target=try_read)
        thread.start()
        thread.join(timeout=timeout_sec)

        if not self.audio_bytes:
            return {"status": "error", "message": "No audio bytes received."}

        amp = sum(self.audio_bytes) / len(self.audio_bytes)
        return {
            "volume_symbol": round(amp % 128, 2),
            "byte_sample": list(self.audio_bytes[:8]),
            "status": "success"
        }

    def get_available_devices(self):
        return {
            "video_devices": self.video_devices,
            "audio_inputs": self.audio_inputs
        }

# === USB Device Detection (global helper) ===
def detect_usb_devices():
    devices = {
        "usb_cameras": [],
        "usb_audio_inputs": []
    }

    # USB Cameras via /sys
    video_root = "/sys/class/video4linux"
    if os.path.isdir(video_root):
        for dev in os.listdir(video_root):
            path = os.path.join(video_root, dev)
            try:
                with open(os.path.join(path, "name"), "r") as f:
                    cam_name = f.read().strip()
                video_path = f"/dev/{dev}"
                if "usb" in os.readlink(path):
                    devices["usb_cameras"].append({"name": cam_name, "path": video_path})
            except:
                continue

    # USB Audio via /proc/asound/cards
    try:
        with open("/proc/asound/cards", "r") as f:
            lines = f.readlines()
        for i in range(0, len(lines), 2):
            name_line = lines[i].strip()
            desc_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
            card = " ".join(name_line.split()[1:]).strip("[]")
            desc = desc_line.strip()
            if "USB" in card or "USB" in desc:
                devices["usb_audio_inputs"].append(f"{card} — {desc}")
    except:
        pass

    return devices
