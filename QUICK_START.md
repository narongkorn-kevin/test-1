# 🚀 Quick Start - Smoke Detector Auto-Placer

## วิธีใช้งาน (30 วินาที)

### 1. ติดตั้ง (ครั้งแรกเท่านั้น)

```bash
pip install -r requirements.txt
chmod +x auto_place_detectors.sh
```

### 2. รันโปรแกรม

```bash
./auto_place_detectors.sh input.dxf
```

**เสร็จแล้ว!** 🎉

### 3. เปิดไฟล์ผลลัพธ์

```
input_with_detectors_FINAL.dxf
```

---

## ตัวอย่าง

```bash
./auto_place_detectors.sh "RCP-FO10,11,12,16-AR-1.dxf"
```

**Output:**
```
✅ Cleaned 443 old detectors
✅ Found 101 rooms  
✅ Placed 99 new detectors
✅ Detectors are WITHIN building bounds!

📂 Output: RCP-FO10,11,12,16-AR-1_with_detectors_FINAL.dxf ⭐
```

---

## นั่นแหละ! ง่ายมาก ๆ

ไม่ต้องตั้งค่าอะไร ไม่ต้องกำหนด layer ไม่ต้องคำนวณ offset

**แค่ใส่ไฟล์ DXF เข้าไป → ได้ผลลัพธ์เลย!**

---

สำหรับการใช้งานแบบ advance ดูไฟล์ `README.md`


