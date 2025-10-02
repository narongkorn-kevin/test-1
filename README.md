# 🔥 Smoke Detector Auto-Placer

โปรแกรมวางตำแหน่ง Smoke Detector อัตโนมัติตามมาตรฐานสากล สำหรับไฟล์ DXF

## ✨ คุณสมบัติ

- ✅ **One Command** - รันคำสั่งเดียวเสร็จ ไม่ต้องตั้งค่าอะไร
- ✅ ลบ detectors เก่าอัตโนมัติ (ถ้ามี)
- ✅ Auto-detect หน่วยวัด (m, mm, ft, in)
- ✅ Auto-detect room layers
- ✅ คำนวณ offset อัตโนมัติ
- ✅ วาง detector ตามมาตรฐาน NFPA 72
- ✅ Export เป็น DXF พร้อมจุด detector

## 📦 การติดตั้ง

```bash
# 1. Clone หรือ download โฟลเดอร์นี้
# 2. ติดตั้ง dependencies
pip install -r requirements.txt

# 3. ทำให้ script รันได้
chmod +x auto_place_detectors.sh
```

## 🚀 วิธีใช้งาน (Super Easy!)

### One Command - เสร็จทันที! ⭐

```bash
./auto_place_detectors.sh input.dxf
```

**แค่นี้เสร็จ!** 🎉

โปรแกรมจะทำทุกอย่างให้อัตโนมัติ:
1. ลบ detectors เก่า (ถ้ามี)
2. วิเคราะห์ไฟล์ DXF
3. วาง smoke detectors ในตำแหน่งที่ถูกต้อง
4. สร้างไฟล์ output

### ผลลัพธ์

ไฟล์ output: `input_with_detectors_FINAL.dxf`

### ตัวอย่าง

```bash
./auto_place_detectors.sh "RCP-FO10,11,12,16-AR-1.dxf"
```

Output:
```
🔥 Smoke Detector Auto-Placer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Cleaned 443 old detectors
✅ Found 101 rooms
✅ Placed 99 new detectors
✅ Output: RCP-FO10,11,12,16-AR-1_with_detectors_FINAL.dxf
```

## 📋 Requirements

- Python 3.7+
- ezdxf
- shapely
- numpy

ติดตั้งทั้งหมด:
```bash
pip install -r requirements.txt
```

## 🎯 มาตรฐานที่รองรับ

- **NFPA 72** (default): ระยะห่าง ~9.1 m (~30 ft)
- **EN 54-14**: ระยะห่าง ~8.66 m
- **CUSTOM**: กำหนดระยะห่างเอง

## ⚙️ Advanced Usage

### ปรับแต่ง parameters (ถ้าต้องการ)

```bash
# ใช้มาตรฐาน EN54-14
python3 smoke_detector_placer.py input_clean.dxf --std EN54-14

# ใช้ hex grid (ประหยัด ~13%)
python3 smoke_detector_placer.py input_clean.dxf --grid hex

# กำหนดระยะห่างเอง (เมตร)
python3 smoke_detector_placer.py input_clean.dxf --spacing 8.0

# Export CSV ด้วย
python3 smoke_detector_placer.py input_clean.dxf --csv detectors.csv
```

### ดูข้อมูลไฟล์ DXF

```bash
python3 smoke_detector_placer.py input.dxf --inspect
```

จะแสดง:
- ขนาดแบบและหน่วยวัด
- Layer ที่มี closed polygons
- จำนวนห้องในแต่ละ layer

## 💡 Tips

1. **ไฟล์ DXF ต้องมีห้องที่ปิด (closed polyline)**
2. **โปรแกรมจะลบ detectors เก่าอัตโนมัติ** ไม่ต้องทำเอง
3. **ไฟล์ output จะมีชื่อ _with_detectors_FINAL.dxf**
4. **เปิดไฟล์ใน AutoCAD แล้ว export เป็น PDF** จะได้คุณภาพดีที่สุด

## 📞 ไฟล์ตัวอย่าง

```bash
./auto_place_detectors.sh "RCP-FO10,11,12,16-AR-1.dxf"
```

ผลลัพธ์:
- 🏠 101 ห้อง
- 🔥 99 detectors
- ✅ วางถูกตำแหน่งทั้งหมด

## 🔧 Troubleshooting

### ถ้าไม่เจอห้อง:
```bash
python3 smoke_detector_placer.py input.dxf --inspect
```
ดู layer ที่มี แล้วระบุ:
```bash
python3 smoke_detector_placer.py input.dxf --rooms-layer YOUR_LAYER
```

### ถ้าหน่วยวัดผิด:
```bash
python3 smoke_detector_placer.py input.dxf --units mm
```

### ถ้าจุดไม่ตรง:
1. รัน `python3 find_visual_offset.py` เพื่อหา offset ที่ถูกต้อง
2. แก้ไข `auto_place_detectors.sh` บรรทัด offset

## 📁 โครงสร้างไฟล์

```
.
├── auto_place_detectors.sh      ⭐ Main script (รันอันนี้!)
├── smoke_detector_placer.py     Core placement engine
├── clean_detectors.py           Cleaner utility
├── verify_final.py              Verification tool
├── find_visual_offset.py        Offset finder
├── requirements.txt             Python dependencies
└── README.md                    This file
```

## 🎓 วิธีทำงาน

1. **Clean** - ลบ smoke detectors เก่าออกจากไฟล์
2. **Analyze** - วิเคราะห์ room layers และ architectural layers
3. **Calculate** - คำนวณ offset เพื่อ align ห้องกับแบบหลัก
4. **Place** - วาง detectors ด้วยระยะห่างตามมาตรฐาน
5. **Export** - สร้างไฟล์ DXF ใหม่พร้อม detector layer

## 📄 License

MIT License - ใช้งานได้อย่างอิสระ

---

**Made with ❤️ for Fire Safety Engineers**

สำหรับคำถามหรือปัญหา ดูไฟล์ `SOLUTION_TH.txt` หรือ `USAGE_TH.txt`
