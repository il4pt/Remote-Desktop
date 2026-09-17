import asyncio
import base64
import io
import json
import os
import platform
import socket
import subprocess
import sys
import time
import uuid
import psutil
import requests
import websockets

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent_config.json")
DEFAULT_SERVER_URL = "http://localhost:8080"
DEFAULT_WS_URL = "ws://localhost:8080"

# Bilgisayarda başlatılabilecek tanımlı uygulamalar
DEFAULT_APPS = [
    {"id": "steam", "name": "Steam", "icon": "fa-brands fa-steam", "cmd_win": "steam", "cmd_linux": "steam"},
    {"id": "chrome", "name": "Google Chrome", "icon": "fa-brands fa-chrome", "cmd_win": "chrome", "cmd_linux": "google-chrome || chromium"},
    {"id": "vscode", "name": "VS Code", "icon": "fa-solid fa-code", "cmd_win": "code", "cmd_linux": "code"},
    {"id": "spotify", "name": "Spotify", "icon": "fa-brands fa-spotify", "cmd_win": "spotify", "cmd_linux": "spotify"},
    {"id": "discord", "name": "Discord", "icon": "fa-brands fa-discord", "cmd_win": "discord", "cmd_linux": "discord"},
    {"id": "terminal", "name": "Terminal", "icon": "fa-solid fa-terminal", "cmd_win": "cmd.exe", "cmd_linux": "x-terminal-emulator || bash"},
]


def get_mac_address() -> str:
    try:
        mac_num = uuid.getnode()
        mac = ':'.join(('%012X' % mac_num)[i:i+2] for i in range(0, 12, 2))
        return mac
    except Exception:
        return "00:00:00:00:00:00"


def get_local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def execute_power_action(action: str):
    current_os = platform.system().lower()
    print(f"\n[RemotePower] Komut yürütülüyor: {action.upper()} ({current_os})")

    if action == "shutdown":
        if current_os == "windows":
            os.system("shutdown /s /t 1")
        elif current_os in ["linux", "darwin"]:
            os.system("systemctl poweroff || sudo poweroff || shutdown -h now")

    elif action == "restart":
        if current_os == "windows":
            os.system("shutdown /r /t 1")
        elif current_os in ["linux", "darwin"]:
            os.system("systemctl reboot || sudo reboot || shutdown -r now")

    elif action == "sleep":
        if current_os == "windows":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif current_os == "darwin":
            os.system("pmset sleepnow")
        elif current_os == "linux":
            os.system("systemctl suspend")

    elif action == "lock":
        if current_os == "windows":
            os.system("rundll32.exe user32.dll,LockWorkStation")
        elif current_os == "darwin":
            os.system("pmset displaysleepnow")
        elif current_os == "linux":
            os.system("loginctl lock-session || xdg-screensaver lock")


def launch_application(app_id: str) -> bool:
    """Telefondan tetiklenen masaüstü uygulamasını çalıştırır"""
    current_os = platform.system().lower()
    app = next((a for a in DEFAULT_APPS if a["id"] == app_id), None)
    if not app:
        print(f"[RemotePower] Bilinmeyen uygulama isteği: {app_id}")
        return False

    cmd = app["cmd_win"] if current_os == "windows" else app["cmd_linux"]
    print(f"[RemotePower] Uygulama başlatılıyor: {app['name']} ({cmd})")
    try:
        subprocess.Popen(cmd, shell=True)
        return True
    except Exception as e:
        print(f"[RemotePower] Uygulama başlatma hatası: {e}")
        return False


def capture_screen_base64() -> str:
    """Canlı masaüstü ekran görüntüsünü düşük bant genişliği için sıkıştırılmış JPEG/base64 olarak yakalar"""
    try:
        from PIL import ImageGrab
        img = ImageGrab.grab()
        # Mobil ekranda hızlı yüklenmesi için ölçeklendir
        img.thumbnail((960, 540))
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=60)
        return "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode("utf-8")
    except Exception as e:
        return ""


def load_or_register_agent(server_url: str) -> dict:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                if "device_id" in config:
                    return config
        except Exception:
            pass

    pc_name = platform.node() or "Benim Bilgisayarım"
    mac = get_mac_address()
    ip = get_local_ip()

    print(f"\n[RemotePower] Yeni cihaz kaydı yapılıyor: '{pc_name}' (MAC: {mac}, IP: {ip})")
    try:
        resp = requests.post(f"{server_url}/api/devices/register", json={
            "name": pc_name,
            "mac_address": mac,
            "ip_address": ip,
            "type": "pc"
        }, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            config = {
                "device_id": data["device_id"],
                "pairing_code": data["pairing_code"],
                "server_url": server_url,
                "name": pc_name,
                "mac": mac,
                "ip": ip
            }
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)

            print(f"\n========================================================")
            print(f" CIHAZ BAŞARIYLA KAYDEDILDI!")
            print(f" Eşleştirme Kodu (PIN):  >>>  {data['pairing_code']}  <<<")
            print(f"========================================================")
            return config
        else:
            print(f"[HATA] Sunucu kayıt hatası: {resp.text}")
            sys.exit(1)
    except Exception as e:
        print(f"[HATA] Sunucuya bağlanılamadı ({server_url}): {e}")
        sys.exit(1)


async def run_agent():
    server_http = os.getenv("REMOTE_SERVER_URL", DEFAULT_SERVER_URL)
    server_ws = os.getenv("REMOTE_WS_URL", DEFAULT_WS_URL)

    config = load_or_register_agent(server_http)
    device_id = config["device_id"]
    ws_endpoint = f"{server_ws}/ws/agent/{device_id}"

    print(f"[RemotePower] Ajan başlatıldı. Bulut Rölesine bağlanılıyor: {ws_endpoint}")

    while True:
        try:
            async with websockets.connect(ws_endpoint) as ws:
                print(f"[RemotePower] Buluta başarıyla bağlandı! Durum: ÇEVRİMİÇİ (ONLINE)")

                while True:
                    cpu_percent = psutil.cpu_percent(interval=None)
                    ram_percent = psutil.virtual_memory().percent
                    
                    heartbeat_data = {
                        "metrics": {
                            "cpu": cpu_percent,
                            "ram": ram_percent,
                            "os": f"{platform.system()} {platform.release()}"
                        },
                        "available_apps": DEFAULT_APPS
                    }

                    await ws.send(json.dumps(heartbeat_data))

                    try:
                        msg = await asyncio.wait_for(ws.recv(), timeout=2.5)
                        command = json.loads(msg)
                        action = command.get("action")

                        if action == "launch_app":
                            app_id = command.get("app_id")
                            if app_id:
                                launch_application(app_id)
                        elif action == "capture_screen":
                            screenshot_b64 = capture_screen_base64()
                            await ws.send(json.dumps({"event": "screen_frame", "frame": screenshot_b64}))
                        elif action in ["shutdown", "restart", "sleep", "lock"]:
                            execute_power_action(action)

                    except asyncio.TimeoutError:
                        continue

        except (websockets.ConnectionClosed, ConnectionRefusedError, OSError) as e:
            print(f"[RemotePower] Bağlantı koptu ({e}). 5 sn sonra yeniden denenecek...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"[RemotePower] Beklenmedik hata: {e}")
            await asyncio.sleep(5)


if __name__ == "__main__":
    try:
        asyncio.run(run_agent())
    except KeyboardInterrupt:
        print("\n[RemotePower] Ajan durduruldu.")
