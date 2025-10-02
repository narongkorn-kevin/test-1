# 🚀 GUI Quick Start - แก้ปัญหาที่พบบ่อย

## 🖥️ เปิด GUI:

```bash
./run_gui.sh
```

---

## ✅ วิธีใช้ที่แนะนำ (หลีกเลี่ยง Error):

### กรณีที่ 1: ไฟล์มี Detectors เก่าอยู่แล้ว

**ถ้าไฟล์มี detectors เก่า แต่อ่านไม่ได้ (มี error):**

1. ✅ **เลือกไฟล์ clean ที่มีอยู่แล้ว**
   ```
   RCP-FO10,11,12,16-AR-1_clean.dxf
   ```

2. ✅ **เช็ค checkbox: "ข้ามการลบ detectors เก่า"**

3. คลิก "เริ่มวาง Smoke Detectors"

4. เสร็จ! ✨

### กรณีที่ 2: ไฟล์ใหม่ที่สะอาด

1. เลือกไฟล์ DXF

2. **เช็ค checkbox: "ข้ามการลบ detectors เก่า"**

3. คลิก "เริ่มวาง Smoke Detectors"

4. เสร็จ! ✨

---

## ❌ ถ้าเจอ Error:

### Error 1: "Clean failed"

**วิธีแก้:**
1. เช็ค ✅ checkbox: "ข้ามการลบ detectors เก่า"
2. ใช้ไฟล์ clean ที่มีอยู่แล้ว หรือ
3. ใช้ไฟล์ original ถ้าสะอาดอยู่แล้ว

### Error 2: "File not found"

**วิธีแก้:**
- ตรวจสอบว่าไฟล์อยู่ที่ไหน
- ลองเลือกไฟล์ใหม่

### Error 3: "Timeout"

**วิธีแก้:**
- ไฟล์ใหญ่เกินไป ใช้ Command Line แทน:
  ```bash
  ./auto_place_detectors.sh input.dxf
  ```

---

## 💡 Tips:

### ✅ วิธีที่ง่ายที่สุด (สำหรับไฟล์ตัวอย่าง):

```bash
# 1. เปิด GUI
./run_gui.sh

# 2. เลือกไฟล์
RCP-FO10,11,12,16-AR-1_clean.dxf

# 3. เช็ค ✅ "ข้ามการลบ detectors เก่า"

# 4. คลิก "เริ่มวาง Smoke Detectors"

# 5. เสร็จ!
```

### ⚙️ ตั้งค่าที่แนะนำ:

- ✅ **เช็ค "ข้ามการลบ detectors เก่า"** (ถ้าไฟล์สะอาดอยู่แล้ว)
- มาตรฐาน: **NFPA 72** (default)
- Grid: **Square** (default)

---

## 🎯 Workflow ที่ใช้งานได้แน่นอน:

### วิธีที่ 1: ใช้ไฟล์ Clean (แนะนำ)

```
Input: RCP-FO10,11,12,16-AR-1_clean.dxf
Options: ✅ ข้ามการลบ detectors เก่า
Output: RCP-FO10,11,12,16-AR-1_clean_with_detectors.dxf
```

### วิธีที่ 2: ใช้ Command Line (ถ้า GUI มีปัญหา)

```bash
python3 smoke_detector_placer.py "RCP-FO10,11,12,16-AR-1_clean.dxf" \
    --rooms-layer 00_VAV_ZONE \
    --offset-x 300001 --offset-y 0 \
    --no-pdf
```

---

## 📁 ไฟล์ที่มีอยู่แล้ว:

คุณมีไฟล์ที่ใช้งานได้อยู่แล้ว:

1. ✅ **`RCP-FO10,11,12,16-AR-1_clean.dxf`**
   - ไฟล์ที่ลบ detectors เก่าแล้ว
   - ใช้ไฟล์นี้กับ GUI ได้เลย

2. ✅ **`RCP-FO10,11,12,16-AR-1_with_detectors_FINAL.dxf`**
   - ไฟล์ผลลัพธ์สำเร็จแล้ว (99 detectors)
   - เปิดใน AutoCAD ได้เลย
   - **ไม่ต้องทำอะไรเพิ่ม!**

---

## 🆘 ต้องการความช่วยเหลือ?

### เช็คว่า GUI ติดตั้งถูกต้อง:

```bash
python3 -c "import tkinter; print('✅ GUI OK')"
```

ถ้า error:
```bash
# macOS:
brew install python-tk@3.11

# Ubuntu/Debian:
sudo apt-get install python3-tk
```

### ดู Log เต็ม:

- ดูใน Log box ของ GUI
- หรือรัน Command Line แทน

---

## 🎉 Success Checklist:

เมื่อสำเร็จจะเห็น:

- ✅ Log แสดง "Found 101 rooms"
- ✅ Log แสดง "Placed 99 detectors"
- ✅ Log แสดง "COMPLIANT WITH NFPA 72"
- ✅ ปุ่ม "เปิดไฟล์ผลลัพธ์" ใช้งานได้
- ✅ มีไฟล์ `*_with_detectors_FINAL.dxf`

---

**สรุป: เช็ค checkbox "ข้ามการลบ detectors เก่า" แล้วจะไม่มี error!** ✨

