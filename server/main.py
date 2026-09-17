import asyncio
import json
import time
from typing import Dict, List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import Config
from auth import create_access_token, verify_token, generate_pairing_code, generate_device_token
from wol import send_magic_packet

app = FastAPI(
    title="RemotePower Cloud Relay API",
    description="App Store ve Google Play uyumlu Uzaktan Bilgisayar Yönetim ve Wake-on-WAN API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Bellek içi cihaz veritabanı (Üretimde PostgreSQL/Redis kullanılabilir)
devices_db: Dict[str, dict] = {}
pairing_codes: Dict[str, str] = {}  # pairing_code -> device_id

# Olay Günlükleri (Activity Logs) & Zamanlayıcılar (Schedules)
activity_logs: List[dict] = [
    {"id": "1", "device_id": "all", "action": "Uygulama Başlatıldı", "status": "info", "time": "15:30:12", "details": "Sistem servisleri hazır"},
    {"id": "2", "device_id": "all", "action": "WoL Köprüsü Dinlemede", "status": "success", "time": "15:31:05", "details": "Port 9 UDP soketi açık"},
]
schedules_db: List[dict] = []

# Aktif WebSocket bağlantıları
active_agent_connections: Dict[str, WebSocket] = {}  # device_id -> WebSocket (PC veya ESP32)
active_client_connections: Dict[str, List[WebSocket]] = {}  # device_id -> List[WebSocket] (Mobil Uygulamalar)


# --- Pydantic Şemaları ---
class RegisterDeviceRequest(BaseModel):
    name: str
    mac_address: Optional[str] = None
    ip_address: Optional[str] = None
    port: Optional[int] = 9
    type: str = "pc"  # "pc", "esp32", "smart_plug"

class PairDeviceRequest(BaseModel):
    pairing_code: str

class PowerCommandRequest(BaseModel):
    action: str  # "wake", "shutdown", "restart", "sleep", "lock"
    mac_address: Optional[str] = None
    ip_address: Optional[str] = None
    port: Optional[int] = 9

class CreateScheduleRequest(BaseModel):
    device_id: str
    action: str = "wake"  # "wake" veya "shutdown"
    time: str  # "08:30"
    days: List[str]  # ["Pzt", "Sal", "Çar", "Per", "Cum"]
    enabled: bool = True



# --- Yardımcı Doğrulama ---
def get_current_user_token(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        # Geliştirme kolaylığı için boş dönülebilir ama store için token doğrulaması
        return {"sub": "demo_user"}
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Geçersiz veya süresi dolmuş oturum")
    return payload


# --- REST Endpoint'leri ---

@app.get("/")
def health_check():
    return {
        "status": "online",
        "service": "RemotePower Cloud Relay API",
        "active_devices": len(devices_db),
        "timestamp": int(time.time())
    }

@app.post("/api/auth/login")
def login_anonymous():
    """Mobil uygulama ilk açıldığında anonim güvenli oturum tokenı üretir"""
    token = create_access_token({"sub": "user_" + str(int(time.time()))})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/api/devices/register")
def register_device(payload: RegisterDeviceRequest):
    """Masaüstü Ajanı veya ESP32 ilk kurulduğunda kendini sunucuya kaydeder ve eşleştirme kodu alır"""
    device_id = generate_device_token()
    pair_code = generate_pairing_code()

    device_data = {
        "id": device_id,
        "name": payload.name,
        "mac_address": payload.mac_address,
        "ip_address": payload.ip_address,
        "port": payload.port,
        "type": payload.type,
        "status": "offline",
        "last_seen": int(time.time()),
        "metrics": {"cpu": 0, "ram": 0, "os": "Unknown"}
    }

    devices_db[device_id] = device_data
    pairing_codes[pair_code] = device_id

    return {
        "device_id": device_id,
        "pairing_code": pair_code,
        "message": "Cihaz kaydedildi. Mobil uygulamadan bu kod ile veya QR kod ile eşleştirebilirsiniz."
    }

@app.post("/api/devices/pair")
def pair_device(payload: PairDeviceRequest, user=Depends(get_current_user_token)):
    """Mobil uygulama 6 haneli kod veya QR taratarak cihazı kütüphanesine ekler"""
    code = payload.pairing_code.upper()
    if code not in pairing_codes:
        raise HTTPException(status_code=404, detail="Geçersiz veya süresi dolmuş eşleştirme kodu")

    device_id = pairing_codes[code]
    device = devices_db.get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Cihaz bulunamadı")

    return {
        "success": True,
        "device": device
    }

@app.get("/api/devices")
def list_devices(user=Depends(get_current_user_token)):
    """Kullanıcının kayıtlı cihazlarını ve canlı durumlarını listeler"""
    current_time = int(time.time())
    for dev in devices_db.values():
        # Belirli süre ping gelmediyse offline işaretle
        if current_time - dev.get("last_seen", 0) > Config.DEVICE_PING_TIMEOUT_SEC:
            dev["status"] = "offline"
    return list(devices_db.values())

@app.post("/api/devices/{device_id}/command")
async def send_command(device_id: str, payload: PowerCommandRequest, user=Depends(get_current_user_token)):
    """
    Mobil uygulamadan bilgisayara/cihaza güç komutu (Aç, Kapat, Yeniden Başlat, vb.) yollar.
    """
    device = devices_db.get(device_id)
    if not device and payload.action != "wake":
        raise HTTPException(status_code=404, detail="Cihaz bulunamadı")

    action = payload.action.lower()

    # 1. Bilgisayarı AÇMA (WAKE) Komutu
    if action == "wake":
        activity_logs.insert(0, {
            "id": str(int(time.time() * 1000)),
            "device_id": device_id,
            "action": "Açılış Sinyali Gönderildi (Wake)",
            "status": "success",
            "time": time.strftime("%H:%M:%S"),
            "details": f"MAC: {payload.mac_address or device.get('mac_address')} IP: {payload.ip_address or device.get('ip_address')}"
        })
        # Öncelik 1: Eğer PC'ye bağlı bir ESP32 / Donanım anahtarı WebSocket üzerinden bağlıysa, ona tetik yolla
        if device_id in active_agent_connections and device and device.get("type") == "esp32":
            ws = active_agent_connections[device_id]
            await ws.send_text(json.dumps({"action": "trigger_power_relay"}))
            return {"success": True, "message": "Fiziksel donanım anahtarı tetiklendi!"}

        # Öncelik 2: Wake-on-LAN Magic Packet Gönderimi
        mac = payload.mac_address or (device.get("mac_address") if device else None)
        target_ip = payload.ip_address or (device.get("ip_address") if device else "255.255.255.255")
        target_port = payload.port or (device.get("port") if device else 9)

        if not mac:
            raise HTTPException(status_code=400, detail="Wake komutu için MAC adresi zorunludur")

        success = send_magic_packet(mac, target_ip, target_port)
        if success:
            if device:
                device["status"] = "booting"
            return {"success": True, "message": f"WoL Magic Packet başarıyla iletildi ({mac})"}
        else:
            raise HTTPException(status_code=500, detail="WoL paketi gönderilirken hata oluştu")

    # 2. Bilgisayarı KAPATMA / YENİDEN BAŞLATMA / KİLİTLEME Komutları (Masaüstü Ajanı Bağlıysa)
    if device_id in active_agent_connections:
        activity_logs.insert(0, {
            "id": str(int(time.time() * 1000)),
            "device_id": device_id,
            "action": f"{action.upper()} Komutu Uygulandı",
            "status": "warning" if action == "shutdown" else "info",
            "time": time.strftime("%H:%M:%S"),
            "details": f"İşletim sistemi sinyali iletildi"
        })
        ws = active_agent_connections[device_id]
        command_data = {"action": action, "timestamp": int(time.time())}
        await ws.send_text(json.dumps(command_data))
        return {"success": True, "message": f"'{action}' komutu bilgisayar ajanına iletildi."}
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Bilgisayar şu anda çevrim dışı görünüyor. '{action}' komutu verilebilmesi için bilgisayarın açık ve ajanının bağlı olması gerekir."
        )


# --- Masaüstü Uygulama Başlatıcı ve Canlı Ekran API'ları ---

class LaunchAppRequest(BaseModel):
    app_id: str

@app.post("/api/devices/{device_id}/launch-app")
async def launch_app(device_id: str, payload: LaunchAppRequest, user=Depends(get_current_user_token)):
    """Bilgisayarda seçilen programı başlatır (Steam, Chrome, VS Code vb.)"""
    if device_id not in active_agent_connections:
        raise HTTPException(status_code=400, detail="Bilgisayar çevrim dışı! Önce bilgisayarı açmalısınız.")
    
    ws = active_agent_connections[device_id]
    await ws.send_text(json.dumps({"action": "launch_app", "app_id": payload.app_id}))
    
    activity_logs.insert(0, {
        "id": str(int(time.time() * 1000)),
        "device_id": device_id,
        "action": f"Uygulama Başlatıldı: {payload.app_id.upper()}",
        "status": "success",
        "time": time.strftime("%H:%M:%S"),
        "details": "Masaüstünde program açıldı"
    })
    return {"success": True, "message": f"'{payload.app_id}' uygulaması bilgisayarınızda başlatıldı."}

@app.get("/api/devices/{device_id}/apps")
def list_apps(device_id: str, user=Depends(get_current_user_token)):
    """Bilgisayarda başlatılabilecek tanımlı programları listeler"""
    device = devices_db.get(device_id)
    if device and "apps" in device:
        return device["apps"]
    # Varsayılan uygulamalar
    return [
        {"id": "steam", "name": "Steam", "icon": "fa-brands fa-steam", "category": "Oyun"},
        {"id": "chrome", "name": "Google Chrome", "icon": "fa-brands fa-chrome", "category": "Tarayıcı"},
        {"id": "vscode", "name": "Visual Studio Code", "icon": "fa-solid fa-code", "category": "Geliştirme"},
        {"id": "spotify", "name": "Spotify", "icon": "fa-brands fa-spotify", "category": "Müzik"},
        {"id": "discord", "name": "Discord", "icon": "fa-brands fa-discord", "category": "İletişim"},
        {"id": "terminal", "name": "Terminal / Komut Satırı", "icon": "fa-solid fa-terminal", "category": "Sistem"},
    ]


# --- Olay Günlüğü ve Zamanlayıcı Endpoint'leri ---

@app.get("/api/logs")
def get_logs(limit: int = 20, user=Depends(get_current_user_token)):
    """Bilgisayar güç açma, kapama ve bağlantı geçmişini listeler"""
    return activity_logs[:limit]

@app.get("/api/schedules")
def get_schedules(user=Depends(get_current_user_token)):
    """Kayıtlı otomatik açılış ve kapanış zamanlayıcılarını listeler"""
    return schedules_db

@app.post("/api/schedules")
def create_schedule(payload: CreateScheduleRequest, user=Depends(get_current_user_token)):
    """Yeni otomatik açma/kapatma zamanı planlar"""
    new_item = {
        "id": "sch_" + str(int(time.time())),
        "device_id": payload.device_id,
        "action": payload.action,
        "time": payload.time,
        "days": payload.days,
        "enabled": payload.enabled,
        "created_at": time.strftime("%Y-%m-%d %H:%M")
    }
    schedules_db.append(new_item)
    return {"success": True, "schedule": new_item}

@app.delete("/api/schedules/{schedule_id}")
def delete_schedule(schedule_id: str, user=Depends(get_current_user_token)):
    global schedules_db
    schedules_db = [s for s in schedules_db if s["id"] != schedule_id]
    return {"success": True}



# --- Gerçek Zamanlı WebSocket Rölesi ---

@app.websocket("/ws/agent/{device_id}")
async def websocket_agent_endpoint(websocket: WebSocket, device_id: str):
    """
    Masaüstü Ajanının (veya ESP32'nin) bağlandığı WebSocket ucu.
    Ajan açıldığında bağlanır, metrik gönderir ve komut bekler.
    """
    await websocket.accept()
    active_agent_connections[device_id] = websocket
    
    # Cihazı hemen online işaretle
    if device_id in devices_db:
        devices_db[device_id]["status"] = "online"
        devices_db[device_id]["last_seen"] = int(time.time())

    # Mobil istemcilere "Bu cihaz artık Online" duyurusu yap
    await notify_mobile_clients(device_id, {"event": "status_change", "status": "online"})

    try:
        while True:
            data_text = await websocket.receive_text()
            data = json.loads(data_text)
            
            # Ping/Heartbeat ve Canlı Metrik Güncellemesi (CPU, RAM vb.)
            if device_id in devices_db:
                devices_db[device_id]["last_seen"] = int(time.time())
                devices_db[device_id]["status"] = "online"
                if "metrics" in data:
                    devices_db[device_id]["metrics"] = data["metrics"]
            
            # Mobil uygulamalara canlı metrikleri akıt
            await notify_mobile_clients(device_id, {"event": "metrics_update", "data": data})

    except WebSocketDisconnect:
        pass
    finally:
        active_agent_connections.pop(device_id, None)
        if device_id in devices_db:
            devices_db[device_id]["status"] = "offline"
        await notify_mobile_clients(device_id, {"event": "status_change", "status": "offline"})


@app.websocket("/ws/client/{device_id}")
async def websocket_client_endpoint(websocket: WebSocket, device_id: str):
    """
    Mobil uygulamanın canlı izleme için bağlandığı WebSocket ucu.
    """
    await websocket.accept()
    if device_id not in active_client_connections:
        active_client_connections[device_id] = []
    active_client_connections[device_id].append(websocket)

    # Anlık durumu hemen gönder
    current_status = devices_db.get(device_id, {}).get("status", "offline")
    await websocket.send_text(json.dumps({"event": "status_change", "status": current_status}))

    try:
        while True:
            # Mobil istemciden gelebilecek anlık istekler
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        if device_id in active_client_connections:
            active_client_connections[device_id].remove(websocket)


async def notify_mobile_clients(device_id: str, message: dict):
    """Cihazı izleyen tüm mobil istemcilere anlık mesaj iletir"""
    clients = active_client_connections.get(device_id, [])
    for client in list(clients):
        try:
            await client.send_text(json.dumps(message))
        except Exception:
            clients.remove(client)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=Config.HOST, port=Config.PORT, reload=True)
