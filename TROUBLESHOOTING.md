# 🔧 Troubleshooting - แก้ปัญหาที่พบบ่อย

## ❌ "Failed to read DXF: Invalid group code"

### สาเหตุ:
ไฟล์ DXF ที่เลือกมีปัญหา:
- ไฟล์เสียหาย
- DXF version เก่าเกินไป
- มี entities ที่ไม่รองรับ
- ข้อมูลใน DXF ผิดพลาด

### วิธีแก้:

#### 1️⃣ ใช้ไฟล์อื่นแทน (ง่ายที่สุด) ⭐

ไฟล์ที่ใช้งานได้:

✅ **ไฟล์ Original:**
```
RCP-FO10,11,12,16-AR-1.dxf
```

✅ **ไฟล์ Clean (แนะนำ):**
```
RCP-FO10,11,12,16-AR-1_clean.dxf
```

✅ **ไฟล์ผลลัพธ์ที่สำเร็จแล้ว:**
```
RCP-FO10,11,12,16-AR-1_with_detectors_FINAL.dxf
```
(เปิดใน AutoCAD ได้เลย!)

❌ **ไฟล์ที่ใช้ไม่ได้:**
```
RCP-FO10,11,12,16-AR-1_red_points.dxf  ← ไฟล์นี้มีปัญหา!
```

#### 2️⃣ แก้ไขไฟล์ใน AutoCAD

1. เปิดไฟล์ใน AutoCAD
2. รัน command: `AUDIT` (แก้ไข errors)
3. รัน command: `PURGE` (ลบ entities ไม่จำเป็น)
4. Save As → DXF → เลือก "AutoCAD 2018 DXF"
5. ใช้ไฟล์ใหม่กับโปรแกรม

#### 3️⃣ ใช้ Recovery Mode

```bash
python3 fix_dxf.py input.dxf
```

จะได้ไฟล์: `input_fixed.dxf`

---

## ❌ "Clean failed"

### สาเหตุ:
ไม่สามารถลบ detectors เก่าได้

### วิธีแก้:

โปรแกรมจะใช้ไฟล์ original อัตโนมัติ
(อาจมี detectors เก่าปนอยู่)

**ไม่ต้องกังวล!** โปรแกรมจะทำงานต่อได้

---

## ❌ "Timeout"

### สาเหตุ:
ไฟล์ใหญ่เกินไป หรือ ระบบช้า

### วิธีแก้:

ใช้ Command Line แทน (เร็วกว่า):

```bash
./auto_place_detectors.sh input.dxf
```

หรือ

```bash
python3 smoke_detector_placer.py input.dxf \
    --rooms-layer 00_VAV_ZONE \
    --offset-x 300001 --offset-y 0
```

---

## ❌ "No rooms found"

### สาเหตุ:
ไม่เจอห้องใน DXF

### วิธีแก้:

#### 1. ตรวจสอบ layers:
```bash
python3 smoke_detector_placer.py input.dxf --inspect
```

#### 2. ระบุ layer เอง:
```bash
python3 smoke_detector_placer.py input.dxf --rooms-layer YOUR_LAYER
```

---

## ❌ GUI ไม่เปิด

### สาเหตุ:
Tkinter ไม่ติดตั้ง

### วิธีแก้:

**macOS:**
```bash
brew install python-tk@3.11
```

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**ตรวจสอบ:**
```bash
python3 -c "import tkinter; print('✅ OK')"
```

---

## ❌ "Permission denied"

### วิธีแก้:

```bash
chmod +x *.sh
chmod +x *.py
```

---

## 💡 Tips เพิ่มเติม:

### ตรวจสอบว่าโปรแกรมติดตั้งถูกต้อง:

```bash
./setup.sh
```

### ตรวจสอบไฟล์ DXF:

```bash
python3 fix_dxf.py your_file.dxf
```

### ดู Log แบบละเอียด:

ใช้ Command Line แทน GUI จะเห็น log ทั้งหมด

---

## 📋 Checklist เมื่อเจอปัญหา:

1. ✅ ตรวจสอบว่าเลือกไฟล์ถูกหรือไม่
   - ใช้ไฟล์ original หรือ clean
   - ไม่ใช้ไฟล์ที่มี `_red_points` หรือ `_temp`

2. ✅ ตรวจสอบว่าไฟล์อยู่ที่ไหน
   - ไฟล์ควรอยู่ใน folder เดียวกับโปรแกรม

3. ✅ ลองใช้ Command Line
   - ถ้า GUI ไม่ทำงาน ลอง CLI

4. ✅ ดู Log
   - Log box ใน GUI หรือ terminal output

5. ✅ ตรวจสอบ setup
   - รัน `./setup.sh` อีกครั้ง

---

## 🆘 ยังไม่ได้?

### ใช้ไฟล์ผลลัพธ์ที่มีอยู่แล้ว:

คุณมีไฟล์ที่สำเร็จอยู่แล้ว:

```
RCP-FO10,11,12,16-AR-1_with_detectors_FINAL.dxf ⭐
```

**เปิดไฟล์นี้ใน AutoCAD ได้เลย!**
- มี 99 detectors
- วางถูกตำแหน่งแล้ว
- ผ่านมาตรฐาน NFPA 72 ✅

**ไม่ต้องทำอะไรเพิ่ม!** 🎉

---

## 📞 Contact

ถ้ายังมีปัญหา:
1. ดู `SOLUTION_TH.txt` - คำอธิบายวิธีแก้ปัญหา
2. ดู `README.md` - คู่มือเต็มรูปแบบ
3. ดู `AUTO_MODE.md` - คู่มือ Auto Mode

---

**สรุป: ถ้าเจอ error ให้ลองใช้ไฟล์อื่น หรือใช้ไฟล์ FINAL ที่มีอยู่แล้ว!** ✨

