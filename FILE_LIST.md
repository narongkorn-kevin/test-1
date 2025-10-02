# 📁 File List - Smoke Detector Auto-Placer

## 🚀 Main Scripts (ใช้งานหลัก)

| File | Description | Usage |
|------|-------------|-------|
| **auto_place_detectors.sh** ⭐ | Main program (One command!) | `./auto_place_detectors.sh input.dxf` |
| **setup.sh** | Setup & install dependencies | `./setup.sh` (run once) |
| **batch_process.sh** | Process multiple files | `./batch_process.sh *.dxf` |
| **demo.sh** | Demo with example file | `./demo.sh` |

## 📚 Documentation (เอกสาร)

| File | Description |
|------|-------------|
| **START_HERE.md** ⭐ | เริ่มต้นใช้งานที่นี่ |
| **QUICK_START.md** | Quick start guide (30 วินาที) |
| **README.md** | Full documentation |
| **SOLUTION_TH.txt** | Technical solution (Thai) |
| **USAGE_TH.txt** | Detailed usage guide (Thai) |
| **FILE_LIST.md** | This file |

## 🔧 Core Programs (โปรแกรมหลัก)

| File | Description |
|------|-------------|
| **smoke_detector_placer.py** | Main detection engine |
| **clean_detectors.py** | Remove old detectors |
| **verify_final.py** | Verification tool |
| **find_visual_offset.py** | Offset calculator |
| **detailed_inspection.py** | Position checker |

## 📦 Other Files

| File | Description |
|------|-------------|
| **requirements.txt** | Python dependencies |
| **quick_start.sh** | Legacy quick start script |
| **run_complete.sh** | Legacy complete workflow |
| **debug_coordinates.py** | Debug tool |
| **check_input.py** | Input file checker |
| **analyze_*.py** | Analysis utilities |

## 📂 Output Files (ไฟล์ที่สร้างขึ้น)

เมื่อรันโปรแกรมจะได้:

| File | Description |
|------|-------------|
| `input_clean.dxf` | Cleaned input file |
| `input_with_detectors_FINAL.dxf` ⭐ | Final output with detectors |

## 🎯 Recommended Workflow:

```bash
# 1. First time setup
./setup.sh

# 2. Read quick start
cat START_HERE.md

# 3. Try demo (optional)
./demo.sh

# 4. Use with your file
./auto_place_detectors.sh your_file.dxf

# 5. Done! Open the output DXF file
```

## 📋 File Sizes:

```
Core scripts:
  auto_place_detectors.sh  5.5K  ⭐ Main
  smoke_detector_placer.py 28K   Core engine
  clean_detectors.py       3.0K  Cleaner
  
Documentation:
  README.md               5.7K  Full guide
  START_HERE.md           3.0K  ⭐ Start here
  QUICK_START.md          1.2K  Quick guide
  
Setup:
  setup.sh                2.8K  Setup script
  requirements.txt        150B  Dependencies
```

## 💡 Tips:

1. **Start with:** `START_HERE.md` or `QUICK_START.md`
2. **Most used:** `./auto_place_detectors.sh input.dxf`
3. **For multiple files:** `./batch_process.sh *.dxf`
4. **Need help?** Check `README.md` or `SOLUTION_TH.txt`

---

**All files are ready to use!** 🚀

Just run: `./auto_place_detectors.sh your_file.dxf`


