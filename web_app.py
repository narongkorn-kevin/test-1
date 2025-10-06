#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Application for Smoke Detector Auto-Placer
Simple upload → process → download interface
"""

from flask import Flask, render_template, request, send_file, jsonify, session
from werkzeug.utils import secure_filename
import os
import sys
import uuid
import shutil
from pathlib import Path
from datetime import datetime
import threading
import time

# Import our smoke detector placer
import ezdxf
from smoke_detector_placer import (
    auto_detect_units,
    auto_detect_room_layers,
    auto_detect_offset,
    unit_scale,
    dxf_to_room_polygons,
    compute_spacing,
    place_detectors_in_room,
    write_output_dxf,
    map_room_names
)

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Store processing status
processing_status = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['dxf']

def process_dxf_file(input_path, output_path, job_id):
    """Process DXF file and place smoke detectors"""
    try:
        processing_status[job_id] = {
            'status': 'processing',
            'progress': 10,
            'message': 'กำลังอ่านไฟล์ DXF...'
        }
        
        # Read DXF file
        doc = ezdxf.readfile(str(input_path))
        
        processing_status[job_id] = {
            'status': 'processing',
            'progress': 20,
            'message': 'กำลังวิเคราะห์หน่วยวัดและ layers...'
        }
        
        # Auto-detect units
        units = auto_detect_units(doc)
        
        # Auto-detect room layers
        room_layers = auto_detect_room_layers(doc)
        
        processing_status[job_id] = {
            'status': 'processing',
            'progress': 40,
            'message': f'พบ {len(room_layers)} layers ที่มีห้อง'
        }
        
        # Get spacing
        spacing_m, spacing_note = compute_spacing("NFPA72", None)
        
        # Calculate scale
        scale = unit_scale(units)
        spacing_units = spacing_m * scale
        margin_units = 0.5 * scale  # default margin
        
        # Get rooms
        rooms = dxf_to_room_polygons(doc, room_layers)
        
        if not rooms:
            processing_status[job_id] = {
                'status': 'error',
                'progress': 0,
                'message': 'ไม่พบห้องในไฟล์ DXF'
            }
            return
        
        processing_status[job_id] = {
            'status': 'processing',
            'progress': 60,
            'message': f'พบ {len(rooms)} ห้อง กำลังคำนวณตำแหน่ง detectors...'
        }
        
        # Auto-detect offset
        offset_x, offset_y = auto_detect_offset(doc, rooms, room_layers)
        
        # Place detectors in each room
        points_by_room = []
        for i, (layer, poly) in enumerate(rooms):
            area_m2 = poly.area / (scale ** 2)
            if area_m2 < 1.0:  # Skip rooms smaller than 1 m²
                continue
            pts = place_detectors_in_room(poly, spacing_units, margin_units, "square")
            points_by_room.append({
                "index": i,
                "layer": layer,
                "name": "",
                "points": pts,
            })
        
        total = sum(len(r["points"]) for r in points_by_room)
        
        processing_status[job_id] = {
            'status': 'processing',
            'progress': 80,
            'message': f'กำลังวาง {total} detectors...'
        }
        
        # Write output DXF
        total_placed = write_output_dxf(doc, Path(output_path), points_by_room, offset_x, offset_y)
        
        processing_status[job_id] = {
            'status': 'completed',
            'progress': 100,
            'message': f'สำเร็จ! วาง {total_placed} detectors ใน {len(points_by_room)} ห้อง',
            'total_rooms': len(rooms),
            'total_detectors': total_placed,
            'output_file': os.path.basename(output_path)
        }
        
    except Exception as e:
        processing_status[job_id] = {
            'status': 'error',
            'progress': 0,
            'message': f'เกิดข้อผิดพลาด: {str(e)}'
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'ไม่มีไฟล์'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'ไม่ได้เลือกไฟล์'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'รองรับเฉพาะไฟล์ .dxf เท่านั้น'}), 400
    
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    
    # Save uploaded file
    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{job_id}_{filename}")
    file.save(input_path)
    
    # Generate output path
    output_filename = f"{Path(filename).stem}_with_detectors.dxf"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{job_id}_{output_filename}")
    
    # Store job info in session
    session[job_id] = {
        'input_path': input_path,
        'output_path': output_path,
        'original_filename': filename,
        'output_filename': output_filename,
        'timestamp': datetime.now().isoformat()
    }
    
    # Initialize processing status
    processing_status[job_id] = {
        'status': 'queued',
        'progress': 0,
        'message': 'รอการประมวลผล...'
    }
    
    # Process in background thread
    thread = threading.Thread(
        target=process_dxf_file,
        args=(input_path, output_path, job_id)
    )
    thread.start()
    
    return jsonify({
        'job_id': job_id,
        'message': 'กำลังประมวลผล...'
    })

@app.route('/status/<job_id>')
def get_status(job_id):
    if job_id not in processing_status:
        return jsonify({'error': 'ไม่พบงานนี้'}), 404
    
    return jsonify(processing_status[job_id])

@app.route('/download/<job_id>')
def download_file(job_id):
    if job_id not in session:
        return "ไม่พบไฟล์", 404
    
    job_info = session[job_id]
    output_path = job_info['output_path']
    
    if not os.path.exists(output_path):
        return "ไฟล์ยังไม่พร้อม", 404
    
    return send_file(
        output_path,
        as_attachment=True,
        download_name=job_info['output_filename']
    )

@app.route('/cleanup/<job_id>', methods=['POST'])
def cleanup(job_id):
    """Clean up temporary files"""
    if job_id in session:
        job_info = session[job_id]
        
        # Delete uploaded file
        if os.path.exists(job_info['input_path']):
            os.remove(job_info['input_path'])
        
        # Delete output file
        if os.path.exists(job_info['output_path']):
            os.remove(job_info['output_path'])
        
        # Remove from session
        session.pop(job_id, None)
    
    # Remove from processing status
    processing_status.pop(job_id, None)
    
    return jsonify({'message': 'ลบไฟล์เรียบร้อย'})

# Periodic cleanup of old files (older than 1 hour)
def cleanup_old_files():
    while True:
        try:
            now = time.time()
            
            # Clean uploads folder
            for filename in os.listdir(app.config['UPLOAD_FOLDER']):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                if os.path.isfile(filepath):
                    if now - os.path.getmtime(filepath) > 3600:  # 1 hour
                        os.remove(filepath)
            
            # Clean outputs folder
            for filename in os.listdir(app.config['OUTPUT_FOLDER']):
                filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
                if os.path.isfile(filepath):
                    if now - os.path.getmtime(filepath) > 3600:  # 1 hour
                        os.remove(filepath)
        except Exception as e:
            print(f"Cleanup error: {e}")
        
        time.sleep(1800)  # Run every 30 minutes

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
cleanup_thread.start()

if __name__ == '__main__':
    print("=" * 60)
    print("🔥 Smoke Detector Web Application")
    print("=" * 60)
    print("📡 เปิดเบราว์เซอร์ที่: http://localhost:4400")
    print("📁 อัพโหลดไฟล์ DXF และดาวน์โหลดไฟล์ที่ประมวลผลเสร็จ")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=4400, threaded=True)

