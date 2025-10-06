#!/bin/bash
# Run Web Application for Smoke Detector Auto-Placer

echo "🔥 Smoke Detector Web Application"
echo "=================================="
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask ยังไม่ได้ติดตั้ง กำลังติดตั้ง..."
    pip3 install flask
    echo ""
fi

# Create necessary folders
mkdir -p uploads outputs templates

echo "🚀 กำลังเปิดเว็บเซิร์ฟเวอร์..."
echo ""
echo "📡 เปิดเบราว์เซอร์ที่: http://localhost:5000"
echo ""
echo "💡 วิธีใช้งาน:"
echo "   1. อัพโหลดไฟล์ DXF"
echo "   2. คลิก 'เริ่มประมวลผล'"
echo "   3. รอจนเสร็จ แล้วดาวน์โหลดไฟล์"
echo ""
echo "กด Ctrl+C เพื่อปิดเซิร์ฟเวอร์"
echo "=================================="
echo ""

python3 web_app.py

