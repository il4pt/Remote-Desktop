import os
import platform
import sys

def install_autostart():
    current_os = platform.system().lower()
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "agent.py"))
    python_exe = sys.executable

    print(f"[RemotePower] Otomatik Başlatma Yapılandırması ({current_os.upper()})")

    if current_os == "windows":
        startup_dir = os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs\Startup")
        bat_file = os.path.join(startup_dir, "RemotePowerAgent.bat")
        with open(bat_file, "w", encoding="utf-8") as f:
            f.write(f'@echo off\nstart "" "{python_exe}" "{script_path}"\n')
        print(f"[BAŞARILI] Windows Başlangıç klasörüne eklendi: {bat_file}")

    elif current_os == "linux":
        service_content = f"""[Unit]
Description=RemotePower Desktop Background Agent
After=network.target

[Service]
Type=simple
User={os.environ.get('USER', 'root')}
ExecStart={python_exe} {script_path}
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
"""
        service_file = os.path.expanduser("~/.config/systemd/user/remotepower.service")
        os.makedirs(os.path.dirname(service_file), exist_ok=True)
        with open(service_file, "w", encoding="utf-8") as f:
            f.write(service_content)
        print(f"[BAŞARILI] Linux user systemd servisi oluşturuldu: {service_file}")
        print("Etkinleştirmek için: systemctl --user enable --now remotepower.service")

    else:
        print("[BILGI] macOS için LaunchAgents plist oluşturabilirsiniz.")

if __name__ == "__main__":
    install_autostart()
