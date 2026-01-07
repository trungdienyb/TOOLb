import os
import sys
import subprocess
import platform
import importlib
import pkgutil
import json
import time
import random
from pathlib import Path

# ===================== RICH UI THEME =====================
class GradientUI:
    """Giao diện gradient với màu sắc đẹp mắt"""
    
    # Màu gradient
    GRADIENT_COLORS = [
        "#ff6b6b", "#ff8e6b", "#ffb26b", "#ffd56b", 
        "#e8ff6b", "#b2ff6b", "#6bff8e", "#6bffb2",
        "#6bffd5", "#6be8ff", "#6bb2ff", "#8e6bff"
    ]
    
    # Màu cố định
    TIME = "bold #a8d5e2"
    SUCCESS = "bold #4ecdc4"
    ERROR = "bold #ff6b6b"
    WARNING = "bold #ffe66d"
    INFO = "bold #6a98f0"
    TITLE = "bold #ffd166"
    SUBTITLE = "#83e1e6"
    
    @staticmethod
    def get_gradient_color(index=0):
        """Lấy màu gradient theo chỉ số"""
        return GradientUI.GRADIENT_COLORS[index % len(GradientUI.GRADIENT_COLORS)]
    
    @staticmethod
    def now():
        """Lấy thời gian hiện tại"""
        import datetime
        return datetime.datetime.now().strftime("%H:%M:%S")

# ===================== AUTO LIB INSTALLER =====================
class AutoLibInstaller:
    """Tự động kiểm tra và cài đặt thư viện"""
    
    # Danh sách thư viện cần thiết với phiên bản tối thiểu
    REQUIRED_LIBS = {
        'requests': '2.28.0',
        'cloudscraper': '1.2.71',
        'rich': '13.0.0',
        'colorama': '0.4.6',
        'urllib3': '1.26.0'
    }
    
    def __init__(self):
        """Khởi tạo installer với Rich console"""
        self._init_rich()
        self.gradient_idx = 0
    
    def _init_rich(self):
        """Khởi tạo Rich console - sẽ thử import hoặc tự cài"""
        try:
            from rich.console import Console
            from rich.panel import Panel
            from rich.text import Text
            from rich.progress import Progress, SpinnerColumn, TextColumn
            from rich.table import Table
            from rich.live import Live
            from rich.box import ROUNDED
            from rich.columns import Columns
            from rich.layout import Layout
            
            self.console = Console()
            self.RichPanel = Panel
            self.RichText = Text
            self.RichTable = Table
            self.RichProgress = Progress
            self.RichSpinnerColumn = SpinnerColumn
            self.RichTextColumn = TextColumn
            self.RichLive = Live
            self.RichBox = ROUNDED
            self.RichColumns = Columns
            self.RichLayout = Layout
            self.rich_available = True
            
        except ImportError:
            # Rich chưa được cài đặt
            self.console = None
            self.rich_available = False
    
    def simulate_loading(self, message="Đang xử lý...", duration=1.5, dots=3):
        """Mô phỏng loading với animation"""
        if self.rich_available and self.console:
            from rich.text import Text
            from rich.live import Live
            
            text = Text()
            for frame in range(dots * 2):
                dots_text = "." * ((frame % dots) + 1)
                text = Text(f"⏳ {message}{dots_text}", style="yellow")
                
                # Tạo Live display
                with Live(text, console=self.console, refresh_per_second=4, transient=True):
                    time.sleep(0.5 / dots)
        else:
            for i in range(dots):
                print(f"\r⏳ {message}{'.' * (i+1)}", end="", flush=True)
                time.sleep(duration / dots)
            print()
    
    def print_header(self):
        """In header với gradient và animation"""
        if self.rich_available and self.console:
            from rich.panel import Panel
            from rich.text import Text
            
            # Animation sequence
            animation_frames = [
                "🚀 BUMX AUTO - LIBRARY INSTALLER",
                "⚡ BUMX AUTO - LIBRARY INSTALLER",
                "✨ BUMX AUTO - LIBRARY INSTALLER",
                "🌟 BUMX AUTO - LIBRARY INSTALLER",
                "🚀 BUMX AUTO - LIBRARY INSTALLER"
            ]
            
            # Hiển thị animation
            for frame in animation_frames:
                # Tạo gradient title
                title_text = Text()
                for i, char in enumerate(frame):
                    color = GradientUI.get_gradient_color(i + self.gradient_idx)
                    title_text.append(char, style=f"bold {color}")
                
                # Tạo subtitle
                subtitle = Text("Tự động kiểm tra & cài đặt thư viện", style=GradientUI.SUBTITLE)
                
                # Panel
                panel = Panel(
                    subtitle,
                    title=title_text,
                    border_style=GradientUI.get_gradient_color(self.gradient_idx + 3),
                    padding=(1, 2),
                    box=self.RichBox
                )
                
                self.console.clear()
                self.console.print(panel)
                time.sleep(0.1)
            
            self.gradient_idx += 1
            
            # Thêm loading effect
            self.simulate_loading("Khởi tạo hệ thống", 1.0)
            
        else:
            # Hiển thị ASCII animation
            frames = [
                "\n" + "=" * 60 + "\n🚀 BUMX AUTO - LIBRARY INSTALLER\n" + "=" * 60,
                "\n" + "=" * 60 + "\n⚡ BUMX AUTO - LIBRARY INSTALLER\n" + "=" * 60,
                "\n" + "=" * 60 + "\n✨ BUMX AUTO - LIBRARY INSTALLER\n" + "=" * 60
            ]
            
            for frame in frames:
                print(frame)
                time.sleep(0.15)
                if frame != frames[-1]:
                    # Xóa dòng
                    print("\033[F" * 4, end="")
    
    def print_step(self, step_number, step_title, step_desc=""):
        """In bước thực hiện với số gradient và loading"""
        if self.rich_available and self.console:
            from rich.text import Text
            from rich.panel import Panel
            
            # Mô phỏng loading trước
            self.simulate_loading(f"Chuẩn bị bước {step_number}", 0.8)
            
            # Màu gradient cho số bước
            step_color = GradientUI.get_gradient_color(step_number)
            
            # Tạo text với animation
            step_text = Text()
            step_text.append(f"📌 STEP {step_number:02d}", style=f"bold {step_color} blink")
            step_text.append(" ── ", style="dim white")
            step_text.append(step_title, style="bold white")
            
            if step_desc:
                step_text.append("\n", style="white")
                step_text.append("├─ ", style="dim cyan")
                step_text.append(step_desc, style="dim white")
            
            # Panel đơn giản
            self.console.print(step_text)
            self.console.print()
            
            # Delay nhẹ
            time.sleep(0.3)
        else:
            print(f"\n[{step_number:02d}] {step_title}")
            if step_desc:
                print(f"     {step_desc}")
            time.sleep(0.5)
    
    def print_status(self, icon, message, status="INFO", details="", delay=0.2):
        """In trạng thái với icon và màu"""
        if self.rich_available and self.console:
            from rich.text import Text
            
            # Màu theo status
            status_colors = {
                "SUCCESS": GradientUI.SUCCESS,
                "ERROR": GradientUI.ERROR,
                "WARNING": GradientUI.WARNING,
                "INFO": GradientUI.INFO
            }
            
            color = status_colors.get(status, GradientUI.INFO)
            
            # Tạo text
            text = Text()
            text.append(f"[{GradientUI.now()}] ", style=GradientUI.TIME)
            text.append(f"{icon} ", style=f"bold {color}")
            text.append(message, style=color)
            
            if details:
                text.append(f" - {details}", style="dim white")
            
            self.console.print(text)
            
            # Delay nhẹ để đọc
            time.sleep(delay)
        else:
            print(f"{icon} {message}")
            if details:
                print(f"    {details}")
            time.sleep(delay)
    
    def print_progress(self, current, total, message):
        """In progress bar với gradient và animation"""
        if self.rich_available and self.console:
            from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
            
            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(complete_style=GradientUI.get_gradient_color(current % 12)),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
                TimeRemainingColumn(),
                console=self.console,
                transient=True,
                expand=True
            ) as progress:
                task = progress.add_task(f"[cyan]{message}", total=total)
                
                # Animated progress
                for i in range(current):
                    progress.update(task, advance=1)
                    time.sleep(0.05)  # Hiệu ứng mượt
        else:
            # ASCII progress bar với animation
            for i in range(current):
                percent = (i + 1) / total * 100
                bar_length = 30
                filled_length = int(bar_length * (i + 1) // total)
                bar = '█' * filled_length + '░' * (bar_length - filled_length)
                
                # Animation characters
                anim_chars = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
                anim = anim_chars[i % len(anim_chars)]
                
                print(f"\r{anim} {message}: [{bar}] {percent:.1f}%", end="", flush=True)
                time.sleep(0.1)
            
            print()
    
    def print_table(self, headers, rows, title=""):
        """In bảng với gradient header và animation"""
        if self.rich_available and self.console:
            from rich.table import Table
            
            # Mô phỏng loading trước khi hiển thị table
            self.simulate_loading("Đang tạo bảng dữ liệu", 0.5)
            
            table = Table(
                title=title,
                title_style=f"bold {GradientUI.TITLE}",
                header_style=f"bold {GradientUI.get_gradient_color(self.gradient_idx)}",
                border_style=GradientUI.SUBTITLE,
                show_lines=True,
                box=self.RichBox
            )
            
            # Thêm headers với animation
            for header in headers:
                table.add_column(header, style="white", header_style="bold")
            
            # Thêm rows với animation từng dòng
            for i, row in enumerate(rows):
                row_style = "white" if i % 2 == 0 else "dim white"
                
                # Hiển thị từng dòng với delay
                table.add_row(*row, style=row_style)
                
                if i == 0:  # Chỉ hiển thị table sau khi có dòng đầu
                    self.console.print(table)
                
                time.sleep(0.1)  # Delay giữa các dòng
            
            self.gradient_idx += 1
        else:
            # ASCII table với animation
            if title:
                print(f"\n{title}")
                time.sleep(0.3)
            
            print("-" * 50)
            time.sleep(0.1)
            
            print(" | ".join(headers))
            time.sleep(0.1)
            
            print("-" * 50)
            time.sleep(0.1)
            
            for i, row in enumerate(rows):
                print(" | ".join(str(x) for x in row))
                time.sleep(0.15)
            
            print("-" * 50)
    
    def print_separator(self, char="─", length=60):
        """In separator với gradient animation"""
        if self.rich_available and self.console:
            from rich.text import Text
            import time
            
            text = Text()
            for i in range(length):
                color = GradientUI.get_gradient_color(i + self.gradient_idx)
                text.append(char, style=f"dim {color}")
                time.sleep(0.005)  # Animation từng ký tự
            
            self.console.print(text)
            self.gradient_idx += 1
        else:
            # ASCII separator với animation
            for i in range(length):
                print(char, end="", flush=True)
                time.sleep(0.01)
            print()
    
    def print_footer(self, success=True, message=""):
        """In footer với animation đầy đủ"""
        if self.rich_available and self.console:
            from rich.panel import Panel
            from rich.text import Text
            import time
            
            # Tạo animation sequence
            frames = 8
            for frame in range(frames):
                # Tạo panel với animation
                if success:
                    icons = ["✅", "✨", "🎉", "🚀", "🌟", "💫", "🎊", "✅"]
                    icon = icons[frame % len(icons)]
                    title_style = "bold green"
                    border_colors = ["#00ff00", "#00ff88", "#00ffee", "#0088ff", "#0000ff", "#8800ff", "#ff00ff", "#00ff00"]
                    border_color = border_colors[frame % len(border_colors)]
                    message_text = message or "TẤT CẢ THƯ VIỆN ĐÃ SẴN SÀNG!"
                else:
                    icons = ["❌", "⚠️", "💥", "🚨", "🔴", "⚡", "🔥", "❌"]
                    icon = icons[frame % len(icons)]
                    title_style = "bold red"
                    border_colors = ["#ff0000", "#ff8800", "#ffaa00", "#ff5500", "#ff0044", "#ff0088", "#ff00aa", "#ff0000"]
                    border_color = border_colors[frame % len(border_colors)]
                    message_text = message or "CÓ LỖI XẢY RA!"
                
                # Tạo text với animation
                panel_text = Text()
                panel_text.append(f"\n{icon} ", style=title_style)
                panel_text.append(message_text, style="bold white")
                panel_text.append(f"\n\n🕒 {GradientUI.now()}", style="dim cyan")
                panel_text.append(f" | 📁 {os.getcwd()}", style="dim white")
                panel_text.append(f" | 🐍 {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}", style="dim green")
                
                panel = Panel(
                    panel_text,
                    border_style=border_color,
                    padding=(1, 2),
                    box=self.RichBox
                )
                
                self.console.clear()
                self.print_header()
                self.console.print(panel)
                time.sleep(0.15)
            
            # Hiển thị cuối cùng lâu hơn
            time.sleep(1.0)
                
        else:
            # ASCII footer với animation
            print("\n" + "=" * 60)
            
            if success:
                success_frames = ["✅", "✨", "🎉", "🚀"]
                for icon in success_frames:
                    print(f"\r{icon} HOÀN THÀNH! {message}", end="", flush=True)
                    time.sleep(0.2)
                print()
            else:
                error_frames = ["❌", "⚠️", "💥", "🚨"]
                for icon in error_frames:
                    print(f"\r{icon} CÓ LỖI! {message}", end="", flush=True)
                    time.sleep(0.2)
                print()
            
            print("=" * 60)
    
    # ===================== CORE METHODS =====================
    
    @staticmethod
    def detect_environment():
        """Phát hiện môi trường đang chạy"""
        env_info = {
            'os': platform.system(),
            'is_termux': False,
            'is_windows': platform.system() == 'Windows',
            'is_linux': platform.system() == 'Linux',
            'is_mac': platform.system() == 'Darwin',
            'python_version': sys.version_info,
            'architecture': platform.machine(),
            'executable': sys.executable,
            'python_path': sys.executable
        }
        
        # Kiểm tra Termux
        termux_markers = [
            'TERMUX_VERSION' in os.environ,
            'TERMUX_APP_PID' in os.environ,
            str(Path.home()).startswith('/data/data/com.termux'),
            sys.prefix.startswith('/data/data/com.termux'),
            'com.termux' in sys.executable
        ]
        env_info['is_termux'] = any(termux_markers)
        
        return env_info
    
    def check_python_version(self):
        """Kiểm tra phiên bản Python"""
        min_version = (3, 7)
        current_version = sys.version_info
        
        # Mô phỏng kiểm tra
        self.simulate_loading("Kiểm tra phiên bản Python", 1.0)
        
        if current_version < min_version:
            self.print_status("❌", "Python version không đủ", "ERROR", 
                           f"Cần {min_version[0]}.{min_version[1]}+, hiện tại: {current_version[0]}.{current_version[1]}")
            return False
        
        self.print_status("✅", "Python version OK", "SUCCESS", 
                       f"Phiên bản: {current_version[0]}.{current_version[1]}.{current_version[2]}")
        return True
    
    @staticmethod
    def is_lib_installed(lib_name):
        """Kiểm tra thư viện đã cài chưa"""
        try:
            # Thử import
            importlib.import_module(lib_name)
            return True
        except ImportError:
            # Kiểm tra thêm qua pkgutil
            return pkgutil.find_loader(lib_name) is not None
        except Exception:
            return False
    
    @staticmethod
    def run_command(cmd, shell=True):
        """Chạy command và trả về output"""
        try:
            result = subprocess.run(
                cmd,
                shell=shell,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
        except Exception as e:
            return False, "", str(e)
    
    def ensure_pip(self, env_info):
        """Đảm bảo pip đã được cài đặt"""
        self.simulate_loading("Kiểm tra pip", 0.8)
        
        # Kiểm tra pip
        success, output, error = self.run_command(f"{env_info['python_path']} -m pip --version")
        
        if not success:
            self.print_status("⚠️", "Pip chưa được cài đặt", "WARNING")
            
            # Cài đặt pip
            if env_info['is_termux']:
                self.print_status("📦", "Cài đặt pip trên Termux...", "INFO")
                self.simulate_loading("Đang cài đặt pip", 1.5)
                success, output, error = self.run_command("pkg install python-pip -y")
            elif env_info['is_windows']:
                self.print_status("📦", "Cài đặt pip trên Windows...", "INFO")
                self.simulate_loading("Đang cài đặt pip", 1.5)
                success, output, error = self.run_command(f"{env_info['python_path']} -m ensurepip --upgrade")
            else:
                self.print_status("📦", "Cài đặt pip...", "INFO")
                self.simulate_loading("Đang cài đặt pip", 1.5)
                success, output, error = self.run_command(f"{env_info['python_path']} -m ensurepip --upgrade")
            
            if success:
                self.print_status("✅", "Đã cài đặt pip", "SUCCESS")
            else:
                self.print_status("❌", "Không thể cài pip", "ERROR", error[:100])
        
        else:
            self.print_status("✅", "Pip đã được cài đặt", "SUCCESS", output.split('\n')[0] if output else "")
        
        return success
    
    def install_library(self, lib_name, min_version, env_info):
        """Cài đặt thư viện"""
        self.simulate_loading(f"Đang cài đặt {lib_name}", 0.5)
        
        # Tạo lệnh cài đặt
        install_cmds = []
        
        if env_info['is_termux']:
            # Termux
            install_cmds = [
                f"{env_info['python_path']} -m pip install {lib_name}>={min_version} --upgrade",
                f"pip install {lib_name}>={min_version} --upgrade"
            ]
        elif env_info['is_windows']:
            # Windows
            install_cmds = [
                f"{env_info['python_path']} -m pip install {lib_name}>={min_version} --upgrade",
                f"py -m pip install {lib_name}>={min_version} --upgrade",
                f"pip install {lib_name}>={min_version} --upgrade"
            ]
        else:
            # Linux/Mac
            install_cmds = [
                f"{env_info['python_path']} -m pip install {lib_name}>={min_version} --upgrade --user",
                f"pip3 install {lib_name}>={min_version} --upgrade --user",
                f"python3 -m pip install {lib_name}>={min_version} --upgrade --user"
            ]
        
        # Thử từng lệnh
        for cmd in install_cmds:
            self.simulate_loading(f"Đang chạy lệnh cài đặt", 0.3)
            success, output, error = self.run_command(cmd)
            
            if success:
                self.print_status("✅", f"Đã cài {lib_name}", "SUCCESS")
                return True
            else:
                # Thử cách khác: không chỉ định version
                self.simulate_loading(f"Thử cách cài đặt khác", 0.3)
                alt_cmd = cmd.replace(f">={min_version}", "")
                success, output, error = self.run_command(alt_cmd)
                if success:
                    self.print_status("✅", f"Đã cài {lib_name} (không version)", "SUCCESS")
                    return True
        
        self.print_status("❌", f"Không thể cài {lib_name}", "ERROR")
        return False
    
    def check_and_install_libs(self, env_info):
        """Kiểm tra và cài đặt thư viện"""
        self.print_step(3, "KIỂM TRA VÀ CÀI ĐẶT THƯ VIỆN", "Đang kiểm tra các thư viện Python...")
        
        # Danh sách để báo cáo
        report_rows = []
        
        for idx, (lib_name, min_version) in enumerate(self.REQUIRED_LIBS.items()):
            # Hiển thị progress
            self.print_progress(idx + 1, len(self.REQUIRED_LIBS), f"Kiểm tra {lib_name}")
            
            if self.is_lib_installed(lib_name):
                # Đã cài - kiểm tra version
                try:
                    module = importlib.import_module(lib_name)
                    current_version = getattr(module, '__version__', 'unknown')
                    
                    # So sánh version nếu có packaging
                    try:
                        from packaging import version as packaging_version
                        if current_version != 'unknown':
                            if packaging_version.parse(current_version) >= packaging_version.parse(min_version):
                                status = "✅"
                                details = f"v{current_version} (đủ mới)"
                                report_rows.append([lib_name, current_version, status, details])
                                continue
                            else:
                                # Cần cập nhật
                                self.print_status("🔄", f"{lib_name} cần cập nhật", "WARNING", 
                                               f"{current_version} -> {min_version}")
                                if self.install_library(lib_name, min_version, env_info):
                                    status = "✅"
                                    details = f"v{current_version} -> v{min_version}"
                                else:
                                    status = "⚠️"
                                    details = f"v{current_version} (cập nhật thất bại)"
                        else:
                            status = "✅"
                            details = "đã cài (version unknown)"
                    except ImportError:
                        # Không có packaging module
                        status = "✅"
                        details = f"v{current_version}"
                    
                    report_rows.append([lib_name, current_version, status, details])
                    
                except Exception as e:
                    status = "⚠️"
                    details = f"lỗi: {str(e)[:50]}"
                    report_rows.append([lib_name, "unknown", status, details])
            else:
                # Chưa cài
                self.print_status("❌", f"{lib_name} chưa được cài đặt", "ERROR")
                if self.install_library(lib_name, min_version, env_info):
                    status = "✅"
                    details = f"đã cài v{min_version}"
                else:
                    status = "❌"
                    details = "cài đặt thất bại"
                
                report_rows.append([lib_name, "not installed", status, details])
        
        # In báo cáo
        self.print_table(
            ["Thư viện", "Version", "Trạng thái", "Chi tiết"],
            report_rows,
            "KẾT QUẢ KIỂM TRA THƯ VIỆN"
        )
        
        # Đếm số thư viện đã cài thành công
        success_count = sum(1 for row in report_rows if "✅" in row[2])
        return success_count == len(self.REQUIRED_LIBS)
    
    def final_check(self):
        """Kiểm tra cuối cùng"""
        self.print_step(4, "KIỂM TRA CUỐI CÙNG", "Đang test import các thư viện...")
        
        test_imports = [
            ("import requests", "requests"),
            ("import cloudscraper", "cloudscraper"),
            ("from rich.console import Console", "rich"),
            ("import colorama", "colorama"),
            ("import urllib3", "urllib3"),
        ]
        
        results = []
        all_ok = True
        
        for import_stmt, lib_name in test_imports:
            # Mô phỏng kiểm tra
            self.simulate_loading(f"Kiểm tra {lib_name}", 0.3)
            
            try:
                exec(import_stmt, globals())
                results.append([lib_name, "✅", "Import thành công"])
            except ImportError as e:
                results.append([lib_name, "❌", str(e)[:50]])
                all_ok = False
            except Exception as e:
                results.append([lib_name, "⚠️", f"Lỗi: {str(e)[:50]}"])
                all_ok = False
        
        # Hiển thị kết quả
        self.print_table(
            ["Thư viện", "Kết quả", "Chi tiết"],
            results,
            "KẾT QUẢ KIỂM TRA IMPORT"
        )
        
        return all_ok
    
    def save_config(self, env_info):
        """Lưu cấu hình"""
        self.simulate_loading("Đang lưu cấu hình", 0.5)
        
        config = {
            'environment': env_info,
            'required_libs': self.REQUIRED_LIBS,
            'checked_at': time.strftime("%Y-%m-%d %H:%M:%S"),
            'working_dir': os.getcwd()
        }
        
        try:
            with open('install_config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            self.print_status("💾", "Đã lưu cấu hình", "SUCCESS", "install_config.json")
        except Exception as e:
            self.print_status("⚠️", "Không thể lưu cấu hình", "WARNING", str(e))
    
    def run_full_check(self):
        """Chạy kiểm tra toàn diện"""
        try:
            # 1. Header với animation
            self.print_header()
            time.sleep(0.5)
            
            # 2. Thông tin môi trường
            self.print_step(1, "THÔNG TIN HỆ THỐNG", "Đang thu thập thông tin môi trường...")
            time.sleep(0.3)
            
            env_info = self.detect_environment()
            env_rows = [
                ["Hệ điều hành", env_info['os']],
                ["Architecture", env_info['architecture']],
                ["Python", f"{env_info['python_version'][0]}.{env_info['python_version'][1]}.{env_info['python_version'][2]}"],
                ["Python Path", env_info['python_path']],
                ["Termux", "✅" if env_info['is_termux'] else "❌"],
                ["Windows", "✅" if env_info['is_windows'] else "❌"],
                ["Linux", "✅" if env_info['is_linux'] else "❌"],
                ["macOS", "✅" if env_info['is_mac'] else "❌"]
            ]
            
            self.print_table(
                ["Thông số", "Giá trị"],
                env_rows,
                "THÔNG TIN HỆ THỐNG"
            )
            time.sleep(0.5)
            
            # 3. Kiểm tra Python version
            if not self.check_python_version():
                self.print_footer(False, "Python version không đủ yêu cầu!")
                return False
            
            # 4. Đảm bảo pip
            if not self.ensure_pip(env_info):
                self.print_footer(False, "Không thể cài đặt pip!")
                return False
            
            # 5. Kiểm tra và cài đặt thư viện
            if not self.check_and_install_libs(env_info):
                self.print_footer(False, "Một số thư viện cài đặt không thành công!")
                return False
            
            # 6. Kiểm tra cuối cùng
            if not self.final_check():
                self.print_footer(False, "Một số thư viện import không thành công!")
                return False
            
            # 7. Lưu cấu hình
            self.save_config(env_info)
            
            # 8. Footer thành công với animation
            self.print_footer(True, "TẤT CẢ THƯ VIỆN ĐÃ SẴN SÀNG! 🚀")
            
            # 9. Hiển thị hướng dẫn cuối cùng
            self.print_separator("═", 60)
            
            self.simulate_loading("Đang tạo hướng dẫn", 0.8)
            
            if self.rich_available and self.console:
                from rich.panel import Panel
                from rich.text import Text
                
                guide_text = Text()
                guide_text.append("🎉 CHẠY CHƯƠNG TRÌNH CHÍNH:\n\n", style="bold green")
                guide_text.append("👉 python logic_chinh.py\n", style="bold cyan")
                guide_text.append("   hoặc\n", style="dim white")
                guide_text.append("👉 python3 logic_chinh.py\n\n", style="bold cyan")
                guide_text.append("📌 Lưu ý:\n", style="bold yellow")
                guide_text.append("• Kiểm tra file auth.txt và cookies.json\n", style="white")
                guide_text.append("• Đảm bảo kết nối internet ổn định\n", style="white")
                guide_text.append("• Sử dụng Ctrl+C để dừng chương trình\n", style="white")
                
                guide_panel = Panel(
                    guide_text,
                    title="🚀 HƯỚNG DẪN",
                    border_style="green",
                    padding=(1, 2)
                )
                
                self.console.print(guide_panel)
            else:
                print("\n🎉 CHẠY CHƯƠNG TRÌNH CHÍNH:")
                print("👉 python logic_chinh.py")
                print("   hoặc")
                print("👉 python3 logic_chinh.py")
                print("\n📌 Lưu ý:")
                print("• Kiểm tra file auth.txt và cookies.json")
                print("• Đảm bảo kết nối internet ổn định")
                print("• Sử dụng Ctrl+C để dừng chương trình")
            
            self.print_separator("═", 60)
            
            return True
            
        except KeyboardInterrupt:
            self.print_status("⏹️", "Đã dừng bởi người dùng", "WARNING")
            return False
        except Exception as e:
            self.print_status("💥", f"Lỗi hệ thống: {str(e)}", "ERROR")
            return False

def main():
    """Hàm chính"""
    # Kiểm tra quyền root
    if os.name != 'nt' and os.geteuid() == 0:
        print("⚠️  Warning: Không nên chạy với quyền root!")
        print("   Thoát và chạy lại với user thường")
        sys.exit(1)
    
    installer = AutoLibInstaller()
    
    try:
        success = installer.run_full_check()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n💥 LỖI KHÔNG XÁC ĐỊNH: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()