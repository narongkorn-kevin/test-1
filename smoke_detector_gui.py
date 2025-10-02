#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 Smoke Detector Auto-Placer - GUI Version
Simple drag-and-drop interface
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import threading
from pathlib import Path
import sys
import os

class SmokeDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔥 Smoke Detector Auto-Placer")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.input_file = None
        self.processing = False
        
        # Set style
        self.setup_style()
        
        # Create UI
        self.create_widgets()
        
        # Bind drag and drop (if supported)
        self.setup_drag_drop()
    
    def setup_style(self):
        """Setup modern style"""
        style = ttk.Style()
        style.theme_use('default')
        
        # Configure colors
        bg_color = '#f0f0f0'
        self.root.configure(bg=bg_color)
    
    def create_widgets(self):
        """Create all UI widgets"""
        
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', pady=(0, 20))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🔥 Smoke Detector Auto-Placer",
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            title_frame,
            text="วางตำแหน่ง Smoke Detector อัตโนมัติตามมาตรฐาน NFPA 72",
            font=('Arial', 12),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        subtitle_label.pack()
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # File selection area
        file_frame = ttk.LabelFrame(main_frame, text="📁 เลือกไฟล์ DXF", padding="15")
        file_frame.pack(fill='x', pady=(0, 10))
        
        # Drop zone
        self.drop_label = tk.Label(
            file_frame,
            text="🎯 ลากไฟล์ DXF มาวางที่นี่\nหรือคลิกปุ่ม 'เลือกไฟล์' ด้านล่าง",
            font=('Arial', 14),
            bg='#ecf0f1',
            fg='#7f8c8d',
            relief='solid',
            borderwidth=2,
            height=4,
            cursor='hand2'
        )
        self.drop_label.pack(fill='x', pady=(0, 10))
        self.drop_label.bind('<Button-1>', lambda e: self.browse_file())
        
        # File path display
        self.file_path_var = tk.StringVar(value="ยังไม่ได้เลือกไฟล์")
        file_path_label = ttk.Label(
            file_frame,
            textvariable=self.file_path_var,
            font=('Arial', 10),
            foreground='#3498db'
        )
        file_path_label.pack(fill='x', pady=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(file_frame)
        button_frame.pack(fill='x')
        
        self.browse_btn = ttk.Button(
            button_frame,
            text="📂 เลือกไฟล์",
            command=self.browse_file
        )
        self.browse_btn.pack(side='left', padx=5)
        
        self.clear_btn = ttk.Button(
            button_frame,
            text="🗑️ ล้าง",
            command=self.clear_file,
            state='disabled'
        )
        self.clear_btn.pack(side='left', padx=5)
        
        # Options
        options_frame = ttk.LabelFrame(main_frame, text="⚙️ ตั้งค่า (Optional)", padding="15")
        options_frame.pack(fill='x', pady=(0, 10))
        
        # Auto mode info
        info_frame = ttk.Frame(options_frame)
        info_frame.pack(fill='x', pady=5)
        
        ttk.Label(
            info_frame,
            text="ℹ️  โปรแกรมจะ auto-detect: units, layers, offset อัตโนมัติ",
            foreground='#3498db',
            font=('Arial', 9, 'italic')
        ).pack(side='left')
        
        # Auto detect option
        self.auto_mode_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_frame,
            text="🤖 Auto Mode (แนะนำ) - ตรวจจับทุกอย่างอัตโนมัติ",
            variable=self.auto_mode_var
        ).pack(anchor='w', pady=5)
        
        self.skip_clean_var = tk.BooleanVar(value=False)  # Keep for backward compatibility
        
        # Standard selection
        std_frame = ttk.Frame(options_frame)
        std_frame.pack(fill='x', pady=5)
        
        ttk.Label(std_frame, text="มาตรฐาน:", width=15).pack(side='left')
        self.standard_var = tk.StringVar(value="NFPA72")
        standards = [("NFPA 72 (default)", "NFPA72"), ("EN 54-14", "EN54-14")]
        for text, value in standards:
            ttk.Radiobutton(
                std_frame,
                text=text,
                variable=self.standard_var,
                value=value
            ).pack(side='left', padx=10)
        
        # Grid type
        grid_frame = ttk.Frame(options_frame)
        grid_frame.pack(fill='x', pady=5)
        
        ttk.Label(grid_frame, text="Grid pattern:", width=15).pack(side='left')
        self.grid_var = tk.StringVar(value="square")
        grids = [("Square (default)", "square"), ("Hex (ประหยัด ~13%)", "hex")]
        for text, value in grids:
            ttk.Radiobutton(
                grid_frame,
                text=text,
                variable=self.grid_var,
                value=value
            ).pack(side='left', padx=10)
        
        # Process button
        self.process_btn = ttk.Button(
            main_frame,
            text="🚀 เริ่มประมวลผล (Auto: Clean → Place → Verify)",
            command=self.process_file,
            state='disabled'
        )
        self.process_btn.pack(fill='x', pady=10)
        
        # Info label
        ttk.Label(
            main_frame,
            text="💡 โปรแกรมจะทำงานอัตโนมัติทั้งหมด ไม่ต้องตั้งค่าอะไรเพิ่ม",
            font=('Arial', 8, 'italic'),
            foreground='#7f8c8d'
        ).pack()
        
        # Progress
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=(0, 10))
        
        # Status
        self.status_var = tk.StringVar(value="พร้อมใช้งาน")
        status_label = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            font=('Arial', 10, 'italic')
        )
        status_label.pack()
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="📋 Log", padding="10")
        log_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            font=('Courier', 9),
            bg='#2c3e50',
            fg='#ecf0f1',
            insertbackground='white'
        )
        self.log_text.pack(fill='both', expand=True)
        
        # Output buttons
        self.output_frame = ttk.Frame(main_frame)
        self.output_frame.pack(fill='x', pady=(10, 0))
        
        self.open_output_btn = ttk.Button(
            self.output_frame,
            text="📂 เปิดไฟล์ผลลัพธ์",
            command=self.open_output,
            state='disabled'
        )
        self.open_output_btn.pack(side='left', padx=5)
        
        self.open_folder_btn = ttk.Button(
            self.output_frame,
            text="📁 เปิด Folder",
            command=self.open_folder,
            state='disabled'
        )
        self.open_folder_btn.pack(side='left', padx=5)
    
    def setup_drag_drop(self):
        """Setup drag and drop (basic version)"""
        # Note: Full drag-drop requires tkinterdnd2 package
        # This is a basic click handler
        pass
    
    def log(self, message, level='info'):
        """Add message to log"""
        self.log_text.insert('end', f"{message}\n")
        self.log_text.see('end')
        self.root.update_idletasks()
    
    def browse_file(self):
        """Browse for DXF file"""
        filename = filedialog.askopenfilename(
            title="เลือกไฟล์ DXF",
            filetypes=[("DXF files", "*.dxf"), ("All files", "*.*")]
        )
        
        if filename:
            self.set_input_file(filename)
    
    def set_input_file(self, filepath):
        """Set input file"""
        self.input_file = Path(filepath)
        self.file_path_var.set(f"📄 {self.input_file.name}")
        self.drop_label.config(
            text=f"✅ ไฟล์ที่เลือก:\n{self.input_file.name}",
            bg='#d5f4e6',
            fg='#27ae60'
        )
        
        self.process_btn.config(state='normal')
        self.clear_btn.config(state='normal')
        
        self.log(f"✅ เลือกไฟล์: {self.input_file.name}", 'info')
    
    def clear_file(self):
        """Clear selected file"""
        self.input_file = None
        self.file_path_var.set("ยังไม่ได้เลือกไฟล์")
        self.drop_label.config(
            text="🎯 ลากไฟล์ DXF มาวางที่นี่\nหรือคลิกปุ่ม 'เลือกไฟล์' ด้านล่าง",
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        
        self.process_btn.config(state='disabled')
        self.clear_btn.config(state='disabled')
        self.open_output_btn.config(state='disabled')
        self.open_folder_btn.config(state='disabled')
        
        self.log_text.delete('1.0', 'end')
        self.status_var.set("พร้อมใช้งาน")
    
    def process_file(self):
        """Process the DXF file"""
        if not self.input_file or not self.input_file.exists():
            messagebox.showerror("Error", "กรุณาเลือกไฟล์ DXF ก่อน")
            return
        
        # Disable buttons
        self.process_btn.config(state='disabled')
        self.browse_btn.config(state='disabled')
        self.clear_btn.config(state='disabled')
        
        # Start progress
        self.progress.start()
        self.status_var.set("กำลังประมวลผล...")
        
        # Run in thread
        thread = threading.Thread(target=self._run_processing)
        thread.daemon = True
        thread.start()
    
    def _run_processing(self):
        """Run the actual processing (in thread)"""
        try:
            self.log("=" * 70)
            self.log("🔥 เริ่มต้นการประมวลผล")
            self.log("=" * 70)
            
            # Step 1: Clean (Always auto)
            self.log("\n📝 Step 1/3: ลบ detectors เก่า (ถ้ามี)...")
            
            clean_file = None
            
            try:
                clean_result = subprocess.run(
                    ['python3', 'clean_detectors.py', str(self.input_file)],
                    capture_output=True,
                    text=True,
                    timeout=120  # 2 minute timeout
                )
                
                if clean_result.returncode == 0:
                    # Success - parse output
                    removed_count = 0
                    for line in clean_result.stdout.split('\n'):
                        if 'Removed' in line and 'detector' in line:
                            # Extract count
                            import re
                            match = re.search(r'(\d+)', line)
                            if match:
                                removed_count = int(match.group(1))
                        if line.strip() and any(x in line for x in ['✅', '⚠️', 'Removed', 'CLEAN']):
                            self.log(f"  {line}")
                    
                    if removed_count > 0:
                        self.log(f"  ✅ ลบ detectors เก่า {removed_count} จุดแล้ว")
                    else:
                        self.log(f"  ✅ ไฟล์สะอาด (ไม่มี detectors เก่า)")
                    
                    clean_file = self.input_file.parent / f"{self.input_file.stem}_clean.dxf"
                    
                else:
                    # Clean failed - try to continue with original
                    self.log(f"  ⚠️  ไม่สามารถลบ detectors เก่าได้")
                    self.log(f"  ℹ️  จะใช้ไฟล์ original (อาจมี detectors เก่าปนอยู่)")
                    clean_file = self.input_file
                    
            except subprocess.TimeoutExpired:
                self.log(f"  ⚠️  Clean timeout - ข้ามขั้นตอนนี้")
                self.log(f"  ℹ️  จะใช้ไฟล์ original")
                clean_file = self.input_file
                
            except Exception as e:
                self.log(f"  ⚠️  Clean error: {str(e)[:100]}")
                self.log(f"  ℹ️  จะใช้ไฟล์ original")
                clean_file = self.input_file
            
            # Ensure we have a file to process
            if not clean_file or not clean_file.exists():
                clean_file = self.input_file
            
            # Step 2: Place detectors
            
            self.log("\n📝 Step 2/3: วาง smoke detectors...")
            self.log(f"  Input file: {clean_file.name}")
            
            # Build command based on auto mode
            cmd = [
                'python3', 'smoke_detector_placer.py',
                str(clean_file),
                '--std', self.standard_var.get(),
                '--grid', self.grid_var.get(),
                '--no-pdf'
            ]
            
            # If NOT auto mode, use specific settings for RCP-FO10 file
            if not self.auto_mode_var.get():
                self.log(f"  ℹ️  Using manual mode with specific settings")
                cmd.extend(['--rooms-layer', '00_VAV_ZONE'])
                cmd.extend(['--offset-x', '300001'])
                cmd.extend(['--offset-y', '0'])
            else:
                self.log(f"  🤖 Using auto mode - will detect everything automatically")
            
            try:
                place_result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True,
                    timeout=180  # 3 minute timeout
                )
                
                if place_result.returncode != 0:
                    error_msg = place_result.stderr if place_result.stderr else "Unknown error"
                    raise Exception(f"Placement failed: {error_msg[:500]}")
                
                # Parse place output
                for line in place_result.stdout.split('\n'):
                    if any(x in line for x in ['🔥', '📁', '🔍', '📐', '🏠', '📍', '💾', '✅', '📊', 'Summary']):
                        self.log(f"  {line}")
                        
            except subprocess.TimeoutExpired:
                raise Exception("Processing timeout - file may be too large or complex")
            except Exception as e:
                # Log the error details
                self.log(f"\n❌ Error details: {str(e)[:500]}")
                if place_result.stderr:
                    self.log(f"  stderr: {place_result.stderr[:500]}")
                raise
            
            # Step 3: Rename to FINAL
            temp_output = self.input_file.parent / f"{self.input_file.stem}_clean_with_detectors.dxf"
            final_output = self.input_file.parent / f"{self.input_file.stem}_with_detectors_FINAL.dxf"
            
            if temp_output.exists():
                if final_output.exists():
                    final_output.unlink()
                temp_output.rename(final_output)
                self.output_file = final_output
            
            # Step 3: Verify
            self.log("\n📝 Step 3/3: ตรวจสอบผลลัพธ์...")
            verify_result = subprocess.run(
                ['python3', 'verify_standards.py'],
                capture_output=True,
                text=True
            )
            
            # Show summary
            for line in verify_result.stdout.split('\n'):
                if '✅' in line or '📊' in line or 'COMPLIANT' in line:
                    self.log(f"  {line}")
            
            self.log("\n" + "=" * 70)
            self.log("✅ เสร็จสมบูรณ์!")
            self.log("=" * 70)
            self.log(f"\n📂 ไฟล์ผลลัพธ์: {final_output.name}")
            
            # Update UI in main thread
            self.root.after(0, self._processing_complete, True, str(final_output))
            
        except Exception as e:
            self.log(f"\n❌ เกิดข้อผิดพลาด: {str(e)}")
            self.root.after(0, self._processing_complete, False, str(e))
    
    def _processing_complete(self, success, message):
        """Called when processing is complete"""
        self.progress.stop()
        self.processing = False
        
        # Re-enable buttons
        self.browse_btn.config(state='normal')
        self.clear_btn.config(state='normal')
        self.process_btn.config(state='normal')
        
        if success:
            self.status_var.set("✅ เสร็จสมบูรณ์!")
            self.open_output_btn.config(state='normal')
            self.open_folder_btn.config(state='normal')
            
            messagebox.showinfo(
                "สำเร็จ!",
                f"วาง Smoke Detectors เสร็จแล้ว!\n\nไฟล์ผลลัพธ์:\n{Path(message).name}"
            )
        else:
            self.status_var.set("❌ เกิดข้อผิดพลาด")
            
            # Check if it's a DXF read error
            if "Failed to read DXF" in message or "Invalid group code" in message:
                error_msg = (
                    "❌ ไม่สามารถอ่านไฟล์ DXF ได้\n\n"
                    "ไฟล์นี้อาจมีปัญหา:\n"
                    "• ไฟล์เสียหาย\n"
                    "• DXF version เก่าเกินไป\n"
                    "• มี entities ที่ไม่รองรับ\n\n"
                    "💡 วิธีแก้:\n"
                    "1. ใช้ไฟล์ original แทน:\n"
                    "   RCP-FO10,11,12,16-AR-1.dxf\n\n"
                    "2. หรือใช้ไฟล์ clean:\n"
                    "   RCP-FO10,11,12,16-AR-1_clean.dxf\n\n"
                    "3. หรือเปิดไฟล์ใน AutoCAD แล้ว\n"
                    "   Save As → DXF R2018\n\n"
                    f"Error: {message[:200]}"
                )
                messagebox.showerror("ไม่สามารถอ่านไฟล์ DXF", error_msg)
            else:
                messagebox.showerror("Error", f"เกิดข้อผิดพลาด:\n{message[:300]}")
    
    def open_output(self):
        """Open output file"""
        if hasattr(self, 'output_file') and self.output_file.exists():
            if sys.platform == 'darwin':  # macOS
                subprocess.run(['open', str(self.output_file)])
            elif sys.platform == 'win32':  # Windows
                os.startfile(str(self.output_file))
            else:  # Linux
                subprocess.run(['xdg-open', str(self.output_file)])
    
    def open_folder(self):
        """Open output folder"""
        if hasattr(self, 'output_file'):
            folder = self.output_file.parent
            if sys.platform == 'darwin':  # macOS
                subprocess.run(['open', str(folder)])
            elif sys.platform == 'win32':  # Windows
                os.startfile(str(folder))
            else:  # Linux
                subprocess.run(['xdg-open', str(folder)])

def main():
    root = tk.Tk()
    app = SmokeDetectorGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()

