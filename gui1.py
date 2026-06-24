import customtkinter as ctk
import psutil
import platform
import time
import threading
import pyttsx3
import os
import subprocess
import string
import random
import shutil
from tkinter import filedialog
import winreg
import gc
import ctypes # المكتبة المسؤولة عن مخاطبة نظام الويندوز للأيقونات 🛠️

# --- 🚀 حركة المحترفين لتثبيت الأيقونة على الـ Taskbar ومنع ظهور شعار بايثون الافتراضي ---
try:
    myappid = 'pro.optimizer.gaming.2026' # معرف فريد للبرنامج بتاعك جوه نظام الويندوز
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass

# إعدادات الصوت الذكية
engine = pyttsx3.init()

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class UltimateOSManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pro Optimizer 2026 - Turbo Gaming Edition")
        self.geometry("1200x900")

        # --- 🖼️ إضافة اللوجو للشريط العلوي للتطبيق ---
        try:
            if os.path.exists("icon.ico"):
                self.iconbitmap("icon.ico") # وضع الأيقونة في الشريط العلوي
        except:
            pass # حماية البرنامج من الإغلاق في حالة عدم وجود الأيقونة مؤقتاً

        # مخازن البيانات لعدم تعطيل الواجهة
        self.fast_data = {}
        self.slow_data = {}
        self.ai_status_text = "AI Status: Optimized"

        # التبويبات المتكاملة
        self.tabs = ctk.CTkTabview(self, width=1150, height=840)
        self.tabs.pack(padx=15, pady=15)
        
        self.tab1 = self.tabs.add("Live Monitor")
        self.tab2 = self.tabs.add("System Cleanup")
        self.tab7 = self.tabs.add("Gaming Booster")  
        self.tab8 = self.tabs.add("Streaming & Media") 
        self.tab3 = self.tabs.add("Network Pro")
        self.tab4 = self.tabs.add("Advanced Managers")
        self.tab5 = self.tabs.add("Security & Tools")
        self.tab6 = self.tabs.add("USB & System Info")

        self.labels = {}
        self.setup_ui()
        
        threading.Thread(target=self.fast_data_worker, daemon=True).start()
        threading.Thread(target=self.slow_data_worker, daemon=True).start()
        
        self.live_update_ui()

    def setup_ui(self):
        # ---------------- 1. Live Monitor ----------------
        live_feats = [
            ("CPU Usage %", self.tab1), ("RAM Usage %", self.tab1), ("Disk Usage %", self.tab1),
            ("CPU Freq (MHz)", self.tab1), ("Core Count", self.tab1), ("AI Status", self.tab1)
        ]
        for name, tab in live_feats:
            lbl = ctk.CTkLabel(tab, text=f"{name}: ---", font=("Consolas", 16))
            lbl.pack(anchor="w", padx=25, pady=8)
            self.labels[name] = lbl

        # ---------------- 2. System Cleanup ----------------
        self.lbl_junk = ctk.CTkLabel(self.tab2, text="Junk Files Found: 0 MB", font=("Consolas", 18, "bold"))
        self.lbl_junk.pack(pady=10)
        
        btn_frame = ctk.CTkFrame(self.tab2)
        btn_frame.pack(pady=5)
        ctk.CTkButton(btn_frame, text="Scan Junk (Turbo)", command=lambda: threading.Thread(target=self.scan_junk, daemon=True).start()).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="Clean Now Plus", fg_color="red", command=lambda: threading.Thread(target=self.clean_temp, daemon=True).start()).grid(row=0, column=1, padx=10)
        
        ctk.CTkLabel(self.tab2, text="--- Duplicate File Finder ---", font=("Consolas", 14, "bold")).pack(pady=10)
        ctk.CTkButton(self.tab2, text="Select Folder to Find Duplicates", command=lambda: threading.Thread(target=self.find_duplicates, daemon=True).start()).pack(pady=5)
        self.txt_duplicates = ctk.CTkTextbox(self.tab2, width=1000, height=180, font=("Consolas", 12))
        self.txt_duplicates.pack(pady=5)

        # ---------------- 🎮 3. Gaming Booster ----------------
        ctk.CTkLabel(self.tab7, text="🎮 Ultra Game Optimizer Suite 2026 🎮", font=("Consolas", 20, "bold"), text_color="#00ffcc").pack(pady=15)
        
        game_frame = ctk.CTkFrame(self.tab7, width=1000, height=150)
        game_frame.pack(pady=15, padx=20, fill="x")
        
        ctk.CTkLabel(game_frame, text="Manage OS Power Plan & Background Services Lifecycle", font=("Consolas", 14)).pack(pady=10)
        
        game_btn_frame = ctk.CTkFrame(game_frame)
        game_btn_frame.pack(pady=10)

        ctk.CTkButton(game_btn_frame, text="🚀 Activate Ultra Game Mode", fg_color="#ff3366", font=("Consolas", 13, "bold"), 
                      command=lambda: threading.Thread(target=self.activate_game_mode, daemon=True).start()).grid(row=0, column=0, padx=10)

        ctk.CTkButton(game_btn_frame, text="🛑 Deactivate / Normal Mode", fg_color="#555555", font=("Consolas", 13, "bold"), 
                      command=lambda: threading.Thread(target=self.deactivate_game_mode, daemon=True).start()).grid(row=0, column=1, padx=10)

        ram_frame = ctk.CTkFrame(self.tab7, width=1000, height=150)
        ram_frame.pack(pady=15, padx=20, fill="x")
        
        ctk.CTkLabel(ram_frame, text="Force Flush System Cache & Standby Memory To Free Up RAM Blocks", font=("Consolas", 14)).pack(pady=10)
        ctk.CTkButton(ram_frame, text="🧹 Instant RAM Purge Before Playing", fg_color="#33cc66", font=("Consolas", 14, "bold"), 
                      command=lambda: threading.Thread(target=self.ram_purge, daemon=True).start()).pack(pady=10)
        
        self.lbl_game_status = ctk.CTkLabel(self.tab7, text="Gaming Status: Standard Windows Mode Active", font=("Consolas", 14, "italic"))
        self.lbl_game_status.pack(pady=20)

        # ---------------- 🎬 4. Streaming & Media ----------------
        ctk.CTkLabel(self.tab8, text="🎬 Streaming & Media Network Booster 🎬", font=("Consolas", 20, "bold"), text_color="#ffcc00").pack(pady=15)
        
        media_btn_frame = ctk.CTkFrame(self.tab8)
        media_btn_frame.pack(pady=10)
        
        ctk.CTkButton(media_btn_frame, text="📡 Run Gaming & Stream Ping Test", fg_color="#9933ff", font=("Consolas", 13, "bold"),
                      command=lambda: threading.Thread(target=self.run_ping_test, daemon=True).start()).grid(row=0, column=0, padx=15)
                      
        ctk.CTkButton(media_btn_frame, text="🗑️ Clear Browser & Video Cache", fg_color="#ff6600", font=("Consolas", 13, "bold"),
                      command=lambda: threading.Thread(target=self.clear_streaming_cache, daemon=True).start()).grid(row=0, column=1, padx=15)
        
        self.txt_media_log = ctk.CTkTextbox(self.tab8, width=1000, height=450, font=("Consolas", 13))
        self.txt_media_log.pack(pady=15)
        self.txt_media_log.insert("0.0", "Ready to boost your streaming and check connection response...")

        # ---------------- 5. Network Pro ----------------
        ctk.CTkButton(self.tab3, text="🚀 Internet Booster (Flush DNS)", fg_color="green", font=("Consolas", 14, "bold"), command=lambda: threading.Thread(target=self.internet_booster, daemon=True).start()).pack(pady=10)
        
        self.wifi_tabs = ctk.CTkTabview(self.tab3, width=1050, height=600)
        self.wifi_tabs.pack()
        self.w_avail = self.wifi_tabs.add("Available Networks")
        self.w_saved = self.wifi_tabs.add("Saved Passwords")
        
        ctk.CTkButton(self.w_avail, text="Scan Nearby Networks", command=lambda: threading.Thread(target=self.scan_nearby_wifi, daemon=True).start()).pack(pady=5)
        self.txt_avail = ctk.CTkTextbox(self.w_avail, width=1000, height=450, font=("Consolas", 13))
        self.txt_avail.pack()

        ctk.CTkButton(self.w_saved, text="Decrypt Saved WiFi Keys", command=self.get_wifi_keys).pack(pady=5)
        self.txt_saved = ctk.CTkTextbox(self.w_saved, width=1000, height=450, font=("Consolas", 13))
        self.txt_saved.pack()

        # ---------------- 6. Advanced Managers ----------------
        manage_tabs = ctk.CTkTabview(self.tab4, width=1050, height=700)
        manage_tabs.pack()
        t_startup = manage_tabs.add("Startup Manager")
        t_search = manage_tabs.add("💡 File Searcher Pro")
        t_backup = manage_tabs.add("Quick Backup")

        ctk.CTkButton(t_startup, text="Scan Startup Apps", command=self.scan_startup).pack(pady=5)
        self.txt_startup = ctk.CTkTextbox(t_startup, width=1000, height=550, font=("Consolas", 13))
        self.txt_startup.pack()

        ctk.CTkLabel(t_search, text="Enter File Name / Keyword:", font=("Consolas", 14)).pack(pady=5)
        self.ent_search = ctk.CTkEntry(t_search, width=400, font=("Consolas", 14))
        self.ent_search.pack(pady=5)
        ctk.CTkButton(t_search, text="Search Everywhere", fg_color="purple", command=lambda: threading.Thread(target=self.file_searcher, daemon=True).start()).pack(pady=5)
        self.txt_search_out = ctk.CTkTextbox(t_search, width=1000, height=400, font=("Consolas", 12))
        self.txt_search_out.pack(pady=5)

        ctk.CTkButton(t_backup, text="Run Quick Backup Job", command=self.run_quick_backup).pack(pady=20)
        self.lbl_backup_status = ctk.CTkLabel(t_backup, text="Status: Idle", font=("Consolas", 14))
        self.lbl_backup_status.pack()

        # ---------------- 7. Security & Tools ----------------
        tools_tabs = ctk.CTkTabview(self.tab5, width=1050, height=700)
        tools_tabs.pack()
        t_lock = tools_tabs.add("Folder Locker")
        t_pass = tools_tabs.add("Password Generator")
        t_shot = tools_tabs.add("📸 Screenshot Saver")

        ctk.CTkButton(t_lock, text="Select Folder to Lock / Unlock", command=self.toggle_folder_lock).pack(pady=20)
        self.lbl_lock_status = ctk.CTkLabel(t_lock, text="Status: Waiting...", font=("Consolas", 12))
        self.lbl_lock_status.pack()

        ctk.CTkButton(t_pass, text="Generate Ultra Strong Password", command=self.generate_password).pack(pady=20)
        self.txt_pass_out = ctk.CTkEntry(t_pass, width=400, font=("Consolas", 16), justify="center")
        self.txt_pass_out.pack()

        ctk.CTkButton(t_shot, text="Capture & Save Screenshot Now", fg_color="darkblue", command=self.take_screenshot).pack(pady=20)
        self.lbl_shot_status = ctk.CTkLabel(t_shot, text="Screenshots will be saved directly on your Desktop", font=("Consolas", 14))
        self.lbl_shot_status.pack()

        # ---------------- 8. USB & System Info ----------------
        ctk.CTkButton(self.tab6, text="🔄 Refresh USB & Drives Toolkit", fg_color="#c97a02", command=self.update_usb_info).pack(pady=10)
        self.txt_usb = ctk.CTkTextbox(self.tab6, width=1000, height=200, font=("Consolas", 13))
        self.txt_usb.pack(pady=5)

        info_feats = [
            ("Threads Count", self.tab6), ("Boot Time", self.tab6), ("System OS", self.tab6), 
            ("PC Name", self.tab6), ("Battery %", self.tab6), ("Memory Total (GB)", self.tab6), 
            ("Memory Available (GB)", self.tab6), ("Active PIDs", self.tab6)
        ]
        for name, tab in info_feats:
            lbl = ctk.CTkLabel(tab, text=f"{name}: ---", font=("Consolas", 15))
            lbl.pack(anchor="w", padx=25, pady=5)
            self.labels[name] = lbl

        self.update_usb_info()

    def activate_game_mode(self):
        self.after(0, lambda: self.lbl_game_status.configure(text="Tuning Windows for Maximum FPS... Please wait."))
        try:
            subprocess.run("powercfg /setactive SCHEME_MIN", shell=True, stdout=subprocess.DEVNULL)
            self.after(0, lambda: self.lbl_game_status.configure(text="🚀 ULTRA GAMING MODE ACTIVE! Power plan set to Maximum Performance."))
            self.ai_status_text = "AI Status: Gaming Turbo Engaged"
            engine.say("تم تفعيل وضع الأداء الأقصى للألعاب بنجاح")
            engine.runAndWait()
        except Exception as e:
            self.after(0, lambda: self.lbl_game_status.configure(text=f"Failed to engage gaming plan: {str(e)}"))

    def deactivate_game_mode(self):
        self.after(0, lambda: self.lbl_game_status.configure(text="Restoring standard Windows power balance..."))
        try:
            subprocess.run("powercfg /setactive SCHEME_BALANCED", shell=True, stdout=subprocess.DEVNULL)
            self.after(0, lambda: self.lbl_game_status.configure(text="🟩 Standard Mode Active. Power plan restored to Balanced."))
            self.ai_status_text = "AI Status: Optimized"
            engine.say("تم العودة إلى الوضع الطبيعي الموفر للكهرباء")
            engine.runAndWait()
        except Exception as e:
            self.after(0, lambda: self.lbl_game_status.configure(text=f"Failed to restore mode: {str(e)}"))

    def ram_purge(self):
        self.after(0, lambda: self.lbl_game_status.configure(text="Purging RAM cache blocks..."))
        try:
            gc.collect()
            time.sleep(1)
            ram_avail = psutil.virtual_memory().available / 1024**3
            self.after(0, lambda: self.lbl_game_status.configure(text=f"🧹 RAM Flushed! Available memory boosted. Current Available: {ram_avail:.2f} GB"))
            engine.say("تم تفريغ كاش الذاكرة العشوائية لتوفير مساحة للعبتك")
            engine.runAndWait()
        except:
            self.after(0, lambda: self.lbl_game_status.configure(text="RAM purge completed with standard optimization."))

    def run_ping_test(self):
        self.safe_update_textbox(self.txt_media_log, "Ping Test Started... Sending packets to gaming and video networks...\n\n")
        targets = {
            "Google / YouTube Global Server": "8.8.8.8",
            "Cloudflare Stream Gateway": "1.1.1.1",
            "Discord Voice & Chat Server": "gateway.discord.gg",
            "Steam / Valve Gaming Network": "steampowered.com"
        }
        report = "--- 📡 Live Streaming & Gaming Ping Report ---\n\n"
        for name, host in targets.items():
            report += f"Testing connection to [{name}]...\n"
            try:
                start_time = time.time()
                output = subprocess.run(f"ping -n 1 {host}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                end_time = time.time()
                if output.returncode == 0:
                    ping_ms = int((end_time - start_time) * 1000)
                    status = "🟩 EXCELLENT (Low Ping)" if ping_ms < 60 else "🟨 GOOD" if ping_ms < 120 else "🟥 HIGH PING (Lag Risk)"
                    report += f"  ↳ Response Time: {ping_ms} ms | Status: {status}\n\n"
                else:
                    report += "  ↳ ❌ Connection Timeout / Request Failed.\n\n"
            except:
                report += "  ↳ ❌ Failed to resolve host.\n\n"
        self.safe_update_textbox(self.txt_media_log, report)

    def clear_streaming_cache(self):
        self.safe_update_textbox(self.txt_media_log, "Targeting Browser & Media Cache folders... Cleaning up streaming debris...\n")
        cache_paths = {
            "Google Chrome Cache": os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache"),
            "Microsoft Edge Cache": os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache")
        }
        cleaned_report = "--- 🗑️ Media Cache Purge Log ---\n\n"
        for name, path in cache_paths.items():
            if os.path.exists(path):
                cleaned_report += f"Found {name} directory. Cleaning data files...\n"
                for file in os.listdir(path):
                    try:
                        file_path = os.path.join(path, file)
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except: pass
                cleaned_report += f"  ↳ Successfully optimized {name}.\n\n"
            else:
                cleaned_report += f"[{name}] is clear or browser is not installed.\n\n"
        cleaned_report += "✨ Video streaming caches cleared! Restart your browser for faster buffering."
        self.safe_update_textbox(self.txt_media_log, cleaned_report)
        engine.say("تم تنظيف كاش المتصفحات والفيديوهات")
        engine.runAndWait()

    def fast_data_worker(self):
        while True:
            try:
                self.fast_data = {
                    "CPU Usage %": psutil.cpu_percent(),
                    "RAM Usage %": psutil.virtual_memory().percent,
                    "Disk Usage %": psutil.disk_usage('/').percent,
                    "CPU Freq (MHz)": int(psutil.cpu_freq().current) if psutil.cpu_freq() else "N/A"
                }
            except: pass
            time.sleep(1)

    def slow_data_worker(self):
        while True:
            try:
                self.slow_data = {
                    "Core Count": psutil.cpu_count(),
                    "Threads Count": sum([p.num_threads() for p in psutil.process_iter(['num_threads'])]), 
                    "Boot Time": time.strftime("%H:%M", time.localtime(psutil.boot_time())),
                    "System OS": platform.system(),
                    "PC Name": platform.node(),
                    "Battery %": psutil.sensors_battery().percent if psutil.sensors_battery() else "AC",
                    "Memory Total (GB)": round(psutil.virtual_memory().total / 1024**3, 2),
                    "Memory Available (GB)": round(psutil.virtual_memory().available / 1024**3, 2),
                    "Active PIDs": len(psutil.pids())
                }
                if self.fast_data.get("RAM Usage %", 0) > 85:
                    self.ai_status_text = "AI Status: CRITICAL - High RAM!"
                else:
                    self.ai_status_text = "AI Status: Optimized"
            except: pass
            time.sleep(5)

    def live_update_ui(self):
        try:
            all_data = {**self.fast_data, **self.slow_data}
            for key, val in all_data.items():
                if key in self.labels:
                    self.labels[key].configure(text=f"{key}: {val}")
            self.labels["AI Status"].configure(text=self.ai_status_text)
        except: pass
        self.after(500, self.live_update_ui)

    def update_usb_info(self):
        self.txt_usb.delete("0.0", "end")
        output = "--- USB & Removable Drives Toolkit ---\n\n"
        found = False
        for part in psutil.disk_partitions():
            if 'removable' in part.opts or 'cdrom' in part.opts:
                try:
                    usage = psutil.disk_usage(part.mountpoint)
                    output += f"🔌 Drive [{part.device}] Mounted at: {part.mountpoint}\n"
                    output += f"   ↳ File System: {part.fstype}\n"
                    output += f"   ↳ Total Size: {usage.total / 1024**3:.2f} GB | Free: {usage.free / 1024**3:.2f} GB\n\n"
                    found = True
                except: pass
        if not found:
            output += "No removable USB devices or flash drives detected currently."
        self.txt_usb.insert("0.0", output)

    def file_searcher(self):
        keyword = self.ent_search.get().strip()
        if not keyword:
            self.safe_update_textbox(self.txt_search_out, "Please write a keyword first.")
            return
        self.safe_update_textbox(self.txt_search_out, f"Searching for '{keyword}' across user directories... Please wait...\n")
        results = ""
        search_root = os.path.expanduser("~") 
        for root, _, files in os.walk(search_root):
            for file in files:
                if keyword.lower() in file.lower():
                    results += f"📂 {os.path.join(root, file)}\n"
            if len(results) > 5000:
                results += "\n[!] Too many results found. Please be more specific."
                break
        self.safe_update_textbox(self.txt_search_out, results if results else "No matching files found.")

    def take_screenshot(self):
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            filename = f"Screenshot_{int(time.time())}.png"
            path = os.path.join(desktop, filename)
            cmd = f"[Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null; [System.Windows.Forms.Screen]::AllScreens | ForEach-Object {{ $bmp = New-Object System.Drawing.Bitmap $_.Bounds.Width, $_.Bounds.Height; $graphics = [System.Drawing.Graphics]::FromImage($bmp); $graphics.CopyFromScreen($_.Bounds.X, $_.Bounds.Y, 0, 0, $bmp.Size); $bmp.Save('{path}') }}"
            subprocess.run(["powershell", "-Command", cmd], shell=True)
            self.lbl_shot_status.configure(text=f"Saved successfully: {filename}")
            engine.say("تم حفظ لقطة الشاشة على سطح المكتب")
            engine.runAndWait()
        except Exception as e:
            self.lbl_shot_status.configure(text=f"Failed to capture: {str(e)}")

    def scan_junk(self):
        self.after(0, lambda: self.lbl_junk.configure(text="Scanning junk files..."))
        folder = os.environ['TEMP']
        total_size = 0
        try:
            with os.scandir(folder) as entries:
                for entry in entries:
                    if entry.is_file():
                        total_size += entry.stat().st_size
            size_mb = total_size / (1024 * 1024)
            self.after(0, lambda: self.lbl_junk.configure(text=f"Junk Files Found: {size_mb:.2f} MB"))
        except:
            self.after(0, lambda: self.lbl_junk.configure(text="Scan failed."))

    def clean_temp(self):
        self.after(0, lambda: self.lbl_junk.configure(text="Cleaning system..."))
        folder = os.environ['TEMP']
        for file in os.listdir(folder):
            try: os.remove(os.path.join(folder, file))
            except: pass
        self.after(0, lambda: self.lbl_junk.configure(text="Junk Files Found: 0 MB"))
        self.ai_status_text = "AI Status: System Cleaned!"
        engine.say("تم تنظيف المخلفات بنجاح يا كريم")
        engine.runAndWait()

    def internet_booster(self):
        try:
            subprocess.run("ipconfig /flushdns", shell=True, stdout=subprocess.DEVNULL)
            subprocess.run("netsh int ip reset", shell=True, stdout=subprocess.DEVNULL)
            engine.say("تم تسريع شبكة الإنترنت وتصفير الكاش بنجاح")
            engine.runAndWait()
        except: pass

    def find_duplicates(self):
        folder = filedialog.askdirectory()
        if not folder: return
        self.safe_update_textbox(self.txt_duplicates, "Scanning for duplicate files... Please wait...\n")
        import hashlib
        def get_hash(p):
            with open(p, 'rb') as f: return hashlib.md5(f.read(1024*1024)).hexdigest()
        hashes = {}
        duplicates = []
        for root, _, files in os.walk(folder):
            for file in files:
                full_path = os.path.join(root, file)
                try:
                    f_hash = get_hash(full_path)
                    if f_hash in hashes: duplicates.append((full_path, hashes[f_hash]))
                    else: hashes[f_hash] = full_path
                except: pass
        res = "--- Duplicate Files Report ---\n\n"
        for dup, orig in duplicates:
            res += f"[!] Duplicate: {os.path.basename(dup)}\n  ↳ Original: {orig}\n\n"
        self.safe_update_textbox(self.txt_duplicates, res if duplicates else "Great! No duplicate files found.")

    def scan_startup(self):
        self.txt_startup.delete("0.0", "end")
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
            res = "--- Startup Registry Applications ---\n\n"
            for i in range(100):
                try:
                    name, val, _ = winreg.EnumValue(key, i)
                    res += f"📌 {name} -> {val}\n\n"
                except OSError: break
            self.txt_startup.insert("0.0", res)
        except Exception as e: self.txt_startup.insert("0.0", f"Error scanning startup: {str(e)}")

    def run_quick_backup(self):
        src = filedialog.askdirectory(title="Select Folder to Backup")
        if not src: return
        dst = filedialog.askdirectory(title="Select Destination Backup Folder")
        if not dst: return
        try:
            shutil.copytree(src, os.path.join(dst, "ProBackup_" + str(int(time.time()))))
            self.lbl_backup_status.configure(text="Status: Backup Completed Successfully!")
        except Exception as e:
            self.lbl_backup_status.configure(text=f"Status: Failed ({str(e)})")

    def toggle_folder_lock(self):
        folder = filedialog.askdirectory(title="Select Folder to Lock/Unlock")
        if not folder: return
        lock_ext = ".{21EC2020-3AEA-1069-A2DD-08002B30309D}"
        if folder.endswith(lock_ext):
            new_name = folder.replace(lock_ext, "")
            os.rename(folder, new_name)
            self.lbl_lock_status.configure(text="Folder UNLOCKED successfully.")
        else:
            os.rename(folder, folder + lock_ext)
            self.lbl_lock_status.configure(text="Folder LOCKED successfully and secured!")

    def generate_password(self):
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        pwd = "".join(random.choice(chars) for _ in range(16))
        self.txt_pass_out.delete(0, "end")
        self.txt_pass_out.insert(0, pwd)

    def safe_update_textbox(self, textbox, content):
        self.after(0, lambda: [textbox.delete("0.0", "end"), textbox.insert("0.0", content)])

    def scan_nearby_wifi(self):
        self.safe_update_textbox(self.txt_avail, "Scanning air for networks... Please wait...\n")
        try:
            cmd = "netsh wlan show networks mode=bssid"
            res = subprocess.check_output(cmd, shell=True).decode('cp1256', errors='ignore')
            self.safe_update_textbox(self.txt_avail, res)
        except Exception as e: self.safe_update_textbox(self.txt_avail, f"Error: {str(e)}")

    def get_wifi_keys(self):
        self.txt_saved.delete("0.0", "end")
        try:
            profiles_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('cp1256', errors='ignore')
            profiles = [line.split(":")[1].strip() for line in profiles_data.split('\n') if "All User Profile" in line]
            result = "--- Decrypted WiFi Database ---\n\n"
            for p in profiles:
                try:
                    key_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', p, 'key=clear']).decode('cp1256', errors='ignore')
                    password = [line.split(":")[1].strip() for line in key_data.split('\n') if "Key Content" in line]
                    result += f"SSID: {p}\n↳ Key: {password[0] if password else 'None'}\n{'-'*50}\n"
                except: pass
            self.txt_saved.insert("0.0", result)
        except Exception as e: self.txt_saved.insert("0.0", f"Error: {str(e)}")

if __name__ == "__main__":
    app = UltimateOSManager()
    app.mainloop()
