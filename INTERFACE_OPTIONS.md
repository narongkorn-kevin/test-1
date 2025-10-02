# 🔥 Smoke Detector Auto-Placer - Interface Options

เลือกวิธีใช้งานที่เหมาะกับคุณ:

---

## 🖥️ Option 1: GUI (Graphical Interface) ⭐ แนะนำ!

**เหมาะสำหรับ:**
- ผู้ใช้ที่ไม่คุ้นเคยกับ command line
- ต้องการความสะดวกสบาย
- ทำงานกับไฟล์ทีละไฟล์

**วิธีเปิด:**
```bash
./run_gui.sh          # macOS/Linux
run_gui.bat           # Windows
```

**Features:**
- ✅ Drag & drop interface
- ✅ Real-time progress
- ✅ เลือกมาตรฐานและ grid pattern
- ✅ เปิดไฟล์ผลลัพธ์ได้ทันที
- ✅ Log แบบ real-time

**ดูคู่มือ:** `GUI_GUIDE.md`

---

## ⌨️ Option 2: Command Line (One Command)

**เหมาะสำหรับ:**
- ผู้ใช้ที่คุ้นเคยกับ terminal
- ต้องการความเร็ว
- Batch processing (หลายไฟล์)

**วิธีใช้:**
```bash
./auto_place_detectors.sh input.dxf
```

**Features:**
- ✅ รันคำสั่งเดียวเสร็จ
- ✅ เร็วและมีประสิทธิภาพ
- ✅ รองรับ batch processing
- ✅ เหมาะสำหรับ automation

**ดูคู่มือ:** `README.md`, `QUICK_START.md`

---

## 🔧 Option 3: Python API (Advanced)

**เหมาะสำหรับ:**
- นักพัฒนาที่ต้องการ integrate
- ต้องการปรับแต่งพฤติกรรม
- สร้าง custom workflows

**วิธีใช้:**
```python
import subprocess

result = subprocess.run([
    'python3', 'smoke_detector_placer.py',
    'input.dxf',
    '--std', 'NFPA72',
    '--grid', 'square'
])
```

**Features:**
- ✅ Full control
- ✅ Scriptable
- ✅ Integration ง่าย

**ดูคู่มือ:** `USAGE_TH.txt`

---

## 📊 Comparison

| Feature | GUI | Command Line | Python API |
|---------|-----|--------------|------------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Speed** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Batch Processing** | ❌ | ✅ | ✅ |
| **Visual Feedback** | ✅ | ⚠️ | ❌ |
| **Customization** | ⚠️ | ✅ | ⭐⭐⭐⭐⭐ |
| **Learning Curve** | ต่ำ | ปานกลาง | สูง |

---

## 💡 Recommendations

**ถ้าคุณเป็น:**

### 🎨 Designer / Architect
→ ใช้ **GUI** (`./run_gui.sh`)

### 👷 Engineer (บ่อยครั้ง)
→ ใช้ **Command Line** (`./auto_place_detectors.sh`)

### 💻 Developer
→ ใช้ **Python API** หรือ **Command Line**

### 🏢 Office Worker
→ ใช้ **GUI** (ง่ายที่สุด!)

---

## 🚀 Quick Start

### GUI (ง่ายที่สุด):
```bash
./run_gui.sh
# → คลิกเลือกไฟล์
# → คลิก "เริ่มวาง Smoke Detectors"
# → เสร็จ!
```

### Command Line (เร็วที่สุด):
```bash
./auto_place_detectors.sh input.dxf
# → เสร็จ!
```

---

## 📞 Help

- **GUI Help:** `cat GUI_GUIDE.md`
- **CLI Help:** `cat README.md`
- **API Help:** `cat USAGE_TH.txt`

---

**Choose your style and start placing detectors!** 🔥
