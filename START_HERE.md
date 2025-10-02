# 🔥 Smoke Detector Auto-Placer

## 🎯 Start Here!

### 🖥️ วิธีที่ 1: ใช้ GUI (แนะนำ - FULL AUTO!) 🤖

```bash
# 1. Setup (ครั้งแรกเท่านั้น)
./setup.sh

# 2. เปิด GUI
./run_gui.sh

# 3. เลือกไฟล์ DXF → กดปุ่ม
# → เสร็จแล้ว!
```

**FULL AUTO!** ไม่ต้องตั้งค่าอะไร แค่เลือกไฟล์และกดปุ่มเดียว! 🎉

โปรแกรมจะทำอัตโนมัติ:
- ✅ ลบ detectors เก่า (ถ้ามี)
- ✅ วาง detectors ใหม่
- ✅ ตรวจสอบมาตรฐาน
- ✅ สร้างไฟล์ผลลัพธ์

**ไม่ต้องทำอะไรเลย!** แค่เลือกไฟล์! 🚀

### ⌨️ วิธีที่ 2: ใช้ Command Line

```bash
# 1. Setup (ครั้งแรกเท่านั้น)
./setup.sh

# 2. รันโปรแกรม
./auto_place_detectors.sh input.dxf

# 3. เปิดไฟล์ผลลัพธ์
# → input_with_detectors_FINAL.dxf
```

**เร็วและเหมาะสำหรับ batch processing!**

---

## 📚 เอกสารทั้งหมด:

| ไฟล์ | คำอธิบาย |
|------|----------|
| **GUI_GUIDE.md** | คู่มือใช้ GUI ⭐ |
| **QUICK_START.md** | เริ่มใช้งานด่วน 30 วินาที |
| **README.md** | คู่มือใช้งานฉบับเต็ม |
| **SOLUTION_TH.txt** | คำอธิบายวิธีแก้ปัญหา (ภาษาไทย) |
| **USAGE_TH.txt** | คู่มือใช้งานภาษาไทยแบบละเอียด |

---

## 🚀 คำสั่งหลัก:

### One File (ใช้บ่อยที่สุด)
```bash
./auto_place_detectors.sh input.dxf
```

### Multiple Files (Batch Processing)
```bash
./batch_process.sh file1.dxf file2.dxf file3.dxf
```

### Advanced (กำหนดค่าเอง)
```bash
python3 smoke_detector_placer.py input.dxf --std EN54-14 --grid hex
```

---

## 💡 Features:

- ✅ **One Command** - รันคำสั่งเดียวเสร็จ
- ✅ **Auto-Detect** - ตรวจจับหน่วยวัด, layers, offset อัตโนมัติ
- ✅ **Clean Old Detectors** - ลบ detectors เก่าอัตโนมัติ
- ✅ **NFPA 72 / EN 54-14** - ตามมาตรฐานสากล
- ✅ **Batch Processing** - ทำทีละหลายไฟล์ได้
- ✅ **Verification** - ตรวจสอบความถูกต้องอัตโนมัติ

---

## 📂 Output:

ไฟล์ที่ได้:
- `input_clean.dxf` - ไฟล์ที่ทำความสะอาดแล้ว
- `input_with_detectors_FINAL.dxf` ⭐ - ไฟล์ผลลัพธ์

Layer ใหม่:
- `SMOKE_DETECTORS` (สีแดง) - จุด smoke detectors

---

## ❓ ต้องการความช่วยเหลือ?

1. **ดู Quick Start:** `cat QUICK_START.md`
2. **ดู README:** `cat README.md`
3. **ดู Examples:** `USAGE_TH.txt`
4. **ดูวิธีแก้ปัญหา:** `SOLUTION_TH.txt`

---

## 🎓 ตัวอย่างการใช้งาน:

```bash
# ติดตั้งครั้งแรก
./setup.sh

# รันโปรแกรม
./auto_place_detectors.sh "RCP-FO10,11,12,16-AR-1.dxf"

# ผลลัพธ์:
# ✅ Cleaned 443 old detectors
# ✅ Found 101 rooms
# ✅ Placed 99 new detectors  
# ✅ Output: RCP-FO10,11,12,16-AR-1_with_detectors_FINAL.dxf
```

---

**Made with ❤️ for Fire Safety Engineers**

พร้อมใช้งานแล้ว! เริ่มจาก `./auto_place_detectors.sh input.dxf` 🚀


