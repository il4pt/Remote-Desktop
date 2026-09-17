# ⚡ RemotePower — Uzaktan Bilgisayar Açma & Yönetim Ekosistemi

<p align="center">
  <img src="https://img.shields.io/badge/iOS-Liquid%20Glass%2018-00F59B?style=for-the-badge&logo=apple&logoColor=white" alt="iOS">
  <img src="https://img.shields.io/badge/Android-Material%20Design%203-80E9BA?style=for-the-badge&logo=android&logoColor=black" alt="Android">
  <img src="https://img.shields.io/badge/Backend-FastAPI%20%2B%20WebSocket-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Protocol-Wake--on--WAN%20%2F%20Magic%20Packet-blue?style=for-the-badge" alt="WoL">
</p>

Dünyanın neresinde olursanız olun (aynı Wi-Fi ağında bulunma zorunluluğu olmadan, hücresel veri dahil), bilgisayarınızı telefonunuzdan tek bir dokunuşla açmanızı, durumunu canlı izlemenizi, masaüstünü anlık izlemenizi ve yüklü programları uzaktan başlatmanızı sağlayan **App Store ve Google Play Store standartlarında** profesyonel bir ekosistem.

---

## 🌟 Öne Çıkan Özellikler

- ⚡ **Uzaktan Güç Açma (Wake-on-WAN & Cloud Switch)**: Kapalı bilgisayarı güvenli Magic Packet veya ESP32 donanım anahtarıyla anında başlatma.
- 📺 **Canlı Masaüstü Ekranı (Live Screen Stream)**: Bilgisayar açıkken telefon ekranından masaüstünü anlık ve canlı olarak izleme.
- 🚀 **Uzaktan Program Başlatıcı (Remote App Launcher)**: Bilgisayarınızdaki oyunları ve yazılımları (Steam, Chrome, VS Code, Spotify, Discord vb.) telefondan tek tıkla açabilme.
- ⏱️ **Akıllı Otomasyon & Güç Geçmişi**:
  - Belirli gün ve saatlerde otomatik açılış/kapanış alarmları planlama.
  - Canlı port ve ağ sağlık ping testi.
  - Saniye saniye güç ve bağlantı olay günlüğü (Activity Log).
- 🍏 **iOS 18 Liquid Glass Tasarımı**: Akışkan sıvı ışıklar, yarı saydam dondurulmuş cam (frosted glass) ve Apple Face ID biyometrik kilidi.
- 🤖 **Android Material You (MD3) Tasarımı**: Google Material Design 3 standartlarında pürüzsüz tonal yüzeyler ve parmak izi güvenliği.
- 🎯 **Açılır Sekme Menüsü (Select Menu Navigation)**: Tüm özellikler arasında akıcı ve modern geçiş.

---

## 📁 Proje Mimarisi

```text
remote open/
├── mobile_app/           # iOS (App Store) ve Android (Play Store) Mobil Uygulaması
│   ├── lib/              # Dashboard, Live Screen, App Launcher, Otomasyon & Ayarlar
│   ├── ios/              # Apple Store standartlarında Info.plist & Podfile
│   └── android/          # Google Play SDK 34 (Android 14) Manifest & Gradle
├── desktop_agent/        # Bilgisayarınızda (Windows/macOS/Linux) Çalışan Arka Plan Ajanı
│   ├── agent.py          # Durum bildiren, ekran yakalayan ve programları başlatan servis
│   └── install_autostart.py # PC açıldığında otomatik başlama yükleyicisi
├── server/               # Bulut Röle & Wake-on-WAN API Sunucusu (FastAPI + WebSocket)
├── firmware_esp32/       # Kapalıyken %100 Açma Garantisi Sağlayan IoT Donanım Firmware'i
├── docs/                 # App Store & Play Store Yayınlama Belgeleri ve Gizlilik Politikası
├── uygulama_onizleme.html # iOS Liquid Glass Canlı İnteraktif Önizleme
└── android_onizleme.html  # Android Material You Canlı İnteraktif Önizleme
```

---

## 🚀 Hızlı Başlangıç

### 1. Canlı Tasarım Önizlemeleri (Tarayıcıda Çalıştırın)
Hiçbir şey yüklemeden arayüzleri, canlı ekranı ve program başlatıcıyı hemen test etmek için:
- **iOS Sürümü İçin**: `uygulama_onizleme.html` dosyasını tarayıcınızda açın.
- **Android Sürümü İçin**: `android_onizleme.html` dosyasını tarayıcınızda açın.

### 2. Bulut Röle Sunucusunu Başlatma
```bash
cd server
pip install -r requirements.txt
python main.py
```
Sunucu `http://localhost:8080` üzerinde REST API ve WebSocket köprüsüyle çalışır.

### 3. Bilgisayarınızda Masaüstü Ajanını Çalıştırma
```bash
cd desktop_agent
pip install -r requirements.txt
python agent.py
```
Ajan açıldığında size 6 haneli bir eşleştirme kodu (PIN) verir. Bilgisayar her açıldığında otomatik başlaması için:
```bash
python install_autostart.py
```

### 4. Mobil Uygulamayı Çalıştırma
```bash
cd mobile_app
flutter pub get
flutter run
```

---

## 📦 GitHub'a Gönderme Komutları

Bu projeyi kendi GitHub reponuza yüklemek için terminalinizden şu adımları izleyin:

```bash
cd "/home/emre/Masaüstü/remote open"
git init
git add .
git commit -m "feat: RemotePower initial release with Live Screen Stream, App Launcher & Select Menu"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADINIZ/REPONUZ.git
git push -u origin main
```

---

## 📄 Lisans
Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.
