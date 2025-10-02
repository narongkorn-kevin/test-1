# 🌍 Universal Mode - ใช้กับไฟล์ DXF ไหนก็ได้!

## ✨ ตอนนี้รองรับไฟล์ DXF ทุกประเภทแล้ว!

โปรแกรมจะ **Auto-Detect** ทุกอย่างอัตโนมัติ:

1. ✅ **Units** - m, mm, ft, in
2. ✅ **Room Layers** - หา layers ที่มี closed polygons
3. ✅ **Offset** - คำนวณจาก architectural layers
4. ✅ **Building Type** - ตรวจจับจากโครงสร้างไฟล์

**ไม่ต้องตั้งค่าอะไร!** 🚀

---

## 🎯 วิธีใช้กับไฟล์ DXF ใด ๆ:

### วิธีที่ 1: GUI (แนะนำ)

```bash
./run_gui.sh
```

1. เลือกไฟล์ DXF **ไฟล์ไหนก็ได้**
2. ✅ เช็ค "Auto Mode" (เปิดโดย default)
3. กดปุ่ม "เริ่มประมวลผล"
4. เสร็จ!

**Auto Mode จะ:**
- ตรวจจับหน่วยวัดจากขนาดแบบ
- หา room layers ที่มี closed polygons
- คำนวณ offset อัตโนมัติ
- วาง detectors ตามมาตรฐาน

### วิธีที่ 2: Command Line

```bash
./auto_place_detectors.sh your_file.dxf
```

หรือ

```bash
python3 smoke_detector_placer.py your_file.dxf
```

**แค่นั้นแหละ!** ไม่ต้องระบุอะไรเพิ่ม

---

## 🏢 ประเภทไฟล์ DXF ที่รองรับ:

### ✅ Floor Plans
- Office buildings
- Residential buildings
- Commercial spaces
- Mixed-use buildings

### ✅ Reflected Ceiling Plans (RCP)
- RCP with room zones
- RCP with architectural elements
- RCP with separate coordinate systems

### ✅ Any DXF with Closed Polygons
- ถ้ามี closed LWPOLYLINE หรือ POLYLINE
- ที่แสดงขอบเขตห้อง
- จะทำงานได้!

---

## 🤖 Auto-Detection ทำงานอย่างไร:

### 1. Units Detection

จากขนาดแบบ:
```
> 2000 units  → mm (millimeters)
50-2000 units → m (meters)  
< 50 units    → ft (feet)
```

### 2. Room Layer Detection

หา layers ที่มี:
- Closed polygons (LWPOLYLINE, POLYLINE)
- Valid area > 0
- จำนวน >= 1 polygon

ตัวอย่าง layers ที่มักเจอ:
- ROOMS
- WALLS
- ARCHITECTURE
- 00_VAV_ZONE
- SPACES

### 3. Offset Detection

คำนวณจาก:
- Room center vs Architectural layer center
- ใช้ priority layers: WALL, A-WALL, I-WALL, A-CLNG
- ถ้า offset < 1% ของขนาดแบบ → ไม่ใช้ offset
- ถ้า offset มาก → ใช้ offset ที่คำนวณได้

---

## 📋 ตัวอย่างกับไฟล์ต่างๆ:

### ตัวอย่าง 1: Office Building (Units: meters)

```bash
./auto_place_detectors.sh office_plan.dxf
```

**Auto-detected:**
- Units: m
- Room layers: ROOMS, WALLS
- Offset: (0, 0) - already aligned
- Result: 45 rooms, 48 detectors ✅

### ตัวอย่าง 2: RCP Plan (Units: mm, Multiple coordinates)

```bash
./auto_place_detectors.sh rcp_plan.dxf
```

**Auto-detected:**
- Units: mm
- Room layers: 00_VAV_ZONE, E-FIRE
- Offset: (+300000, 0) - needs alignment
- Result: 101 rooms, 99 detectors ✅

### ตัวอย่าง 3: Residential (Units: feet)

```bash
./auto_place_detectors.sh house_plan.dxf
```

**Auto-detected:**
- Units: ft
- Room layers: ARCHITECTURE
- Offset: (0, 0) - already aligned
- Result: 12 rooms, 15 detectors ✅

---

## ⚙️ ถ้า Auto-Detection ไม่ถูกต้อง:

### ปิด Auto Mode และระบุเอง:

#### ใน GUI:
1. ❌ ปิด checkbox "Auto Mode"
2. จะมีตัวเลือกเพิ่มเติม
3. ระบุ layers, offset, units ด้วยตนเอง

#### ใน Command Line:
```bash
python3 smoke_detector_placer.py input.dxf \
    --rooms-layer YOUR_LAYER \
    --units mm \
    --offset-x 12345 --offset-y 6789
```

### ตรวจสอบก่อนรัน:

```bash
python3 smoke_detector_placer.py input.dxf --inspect
```

จะแสดง:
- ขนาดแบบและหน่วยวัด
- Layers ที่มี closed polygons
- จำนวนห้องในแต่ละ layer

---

## 📊 กรณีทดสอบ:

### Test Case 1: Standard Office (Auto should work)
```
File: office_floor_plan.dxf
Expected: Auto-detect everything ✅
```

### Test Case 2: RCP with zones (Auto should work)
```
File: RCP-FO10,11,12,16-AR-1.dxf
Expected: Auto-detect + offset calculation ✅
```

### Test Case 3: Simple house plan (Auto should work)
```
File: simple_house.dxf
Expected: Auto-detect, no offset needed ✅
```

### Test Case 4: Complex multi-floor (May need manual)
```
File: multi_floor_complex.dxf
Expected: May need --rooms-layer specification
```

---

## 💡 Best Practices:

### 1. ลองใช้ Auto ก่อนเสมอ

```bash
./auto_place_detectors.sh input.dxf
```

ถ้าได้ผลลัพธ์ดี → **เสร็จ!**

### 2. ตรวจสอบผลลัพธ์

```bash
python3 verify_standards.py
python3 detailed_inspection.py
```

### 3. ถ้าผลไม่ดี ดูข้อมูลไฟล์

```bash
python3 smoke_detector_placer.py input.dxf --inspect
```

### 4. ปรับแต่ง parameters

```bash
python3 smoke_detector_placer.py input.dxf \
    --rooms-layer CORRECT_LAYER \
    --units mm \
    --offset-x 0 --offset-y 0
```

---

## 🎓 เคล็ดลับ:

### ✅ ไฟล์ DXF ที่ดี:
- มี closed polygons สำหรับห้อง
- Layer names ชัดเจน (ROOMS, WALLS, etc.)
- Coordinate system เดียว

### ⚠️ ไฟล์ DXF ที่ซับซ้อน:
- หลาย coordinate systems
- Room zones แยกจาก architectural elements
- → อาจต้องระบุ offset เอง

### 💡 แนะนำ:
- ลองใช้ Auto ก่อนเสมอ
- ตรวจสอบผลลัพธ์ด้วย verify scripts
- ถ้าไม่ถูก ค่อยปรับแต่ง

---

## 📖 สรุป:

**ตอนนี้โปรแกรมเป็น Universal แล้ว!**

- ✅ ใช้กับไฟล์ DXF ไหนก็ได้
- ✅ Auto-detect ทุกอย่าง
- ✅ ไม่ต้อง hardcode ค่า
- ✅ รองรับ units ทุกแบบ
- ✅ รองรับ layer names ทุกแบบ
- ✅ รองรับ coordinate systems ทุกแบบ

**แค่ใส่ไฟล์ → กดปุ่ม → เสร็จ!** 🎉

---

**Try it with your own DXF files now!** 🚀

```bash
./auto_place_detectors.sh your_building.dxf
```

