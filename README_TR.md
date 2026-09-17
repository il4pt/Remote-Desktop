<p align="center">
  <img src="https://img.shields.io/badge/Remote--Desktop-v1.0.0-00F59B?style=for-the-badge&logo=power&logoColor=black" alt="Sürüm">
  <img src="https://img.shields.io/badge/iOS-Liquid%20Glass%2018-00F59B?style=for-the-badge&logo=apple&logoColor=white" alt="iOS">
  <img src="https://img.shields.io/badge/Android-Material%20Design%203-80E9BA?style=for-the-badge&logo=android&logoColor=black" alt="Android">
  <img src="https://img.shields.io/badge/Backend-FastAPI%20%2B%20WebSocket-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Lisans-MIT-blue.svg?style=for-the-badge" alt="Lisans">
</p>

<h1 align="center">⚡ RemotePower / Remote-Desktop</h1>

<p align="center">
  <b>Dünyanın herhangi bir yerinden iPhone ve Android telefonlarınızla bilgisayarınızı uzaktan açmanızı, canlı ekranını izlemenizi, durumunu takip etmenizi ve program başlatmanızı sağlayan profesyonel yönetim ekosistemi.</b>
</p>

<p align="center">
  <a href="README.md">🇬🇧 <b>English</b></a> •
  <a href="README_TR.md">🇹🇷 <b>Türkçe</b></a>
</p>

---

## 📖 Genel Bakış

**Remote-Desktop**, doğrudan **Apple App Store** ve **Google Play Store** standartlarında yayınlanmak üzere tasarlanmış uçtan uca uzaktan güç ve bilgisayar kontrol sistemidir.

Yalnızca aynı ev ağında (Wi-Fi) çalışan geleneksel Wake-on-LAN araçlarının aksine RemotePower, hafif ve güvenli bir **Bulut Röle & WebSocket Sunucusu** üzerinden haberleşir. Bu sayede farklı şehirlerdeyken, hücresel veri (4G/5G) kullanırken bile bilgisayarınızı tek dokunuşla açabilir, masaüstünüzü canlı izleyebilir ve kurulu oyun/programlarınızı uzaktan başlatabilirsiniz.

---

## ✨ Öne Çıkan Özellikler

- ⚡ **İnternet Üzerinden Güç Açma (Wake-on-WAN)**:
  - Kapalı veya uyku modundaki bilgisayarınıza şifreli sihirli paketler (Magic Packet) gönderir.
  - S5 kapalı durumunda %100 fiziksel güç düğmesi basımı için opsiyonel ESP32 donanım anahtarı firmware desteği içerir.
- 📺 **Canlı Masaüstü Ekranı (Live Screen Stream)**:
  - Bilgisayarınızın masaüstünü telefonunuzdan düşük gecikmeyle canlı olarak izleyin (1080p / 30 FPS akış).
  - Programlar açıldığında canlı pencere durumunu ve masaüstünü doğrudan görüntüleyin.
- 🚀 **Uzaktan Program Başlatıcı (Remote App Launcher)**:
  - Bilgisayarınızdaki oyunları ve yazılımları (**Steam, Google Chrome, VS Code, Spotify, Discord, Terminal**) telefonunuzdan tek tıkla çalıştırın.
  - Güvenlik kilidi: Bilgisayar kapalıyken işlem yapılmasını engeller.
- ⏱️ **Akıllı Otomasyon, Zamanlayıcı & Olay Günlüğü**:
  - Belirli gün ve saatlerde otomatik açılış/kapanış alarmları planlayın (Örn: Hafta içi 08:30).
  - Entegre UDP Port 9 bağlantı testi ve canlı ping ölçer.
  - Saniyesi saniyesine gerçek güç ve bağlantı olay geçmişi (Activity Log).
- 🛡️ **Kurumsal Düzey Biyometrik Güvenlik**:
  - iOS tarafında **Apple Face ID / Touch ID** doğrulaması.
  - Android tarafında **Biyometrik Parmak İzi** onayı.
  - JWT ve tek kullanımlık 6 haneli güvenli eşleştirme PIN mimarisi.
- 🎨 **Son Nesil Tasarım Dilleri**:
  - **iOS**: Apple visionOS / iOS 18 **Liquid Glass** estetiği (akışkan sıvı küreleri, buzlu cam derinliği, optik yansımalar ve Dynamic Island).
  - **Android**: Google **Material You (Material Design 3)** standartlarında pürüzsüz tonal yüzeyler, organik butonlar ve obsidyen siyah zemin.
  - **Açılır Menü (Select Menu Navigation)**: Tüm 6 sekme arasında akıcı ve ferah geçiş.

---

## 📁 Proje Dosya Yapısı

```text
Remote-Desktop/
├── mobile_app/               # Flutter Çoklu Platform Uygulaması (iOS & Android)
│   ├── lib/                  # Dart kaynak kodları (Liquid Glass & Material 3)
│   │   ├── screens/          # Dashboard, Canlı Ekran, Program Başlatıcı, Otomasyon, Ayarlar
│   │   ├── widgets/          # Neon Güç Butonu, Sıvı Cam Metrik Kartı
│   │   └── services/         # Bulut API, WebSocket, Biyometrik Doğrulama (LocalAuth)
│   ├── ios/                  # Apple App Store uyumlu Info.plist & Podfile
│   └── android/              # Google Play SDK 34 uyumlu Manifest & Gradle
├── desktop_agent/            # Bilgisayarda Çalışan Arka Plan Ajanı (Windows/macOS/Linux)
│   ├── agent.py              # Durum bildiren, ekran yakalayan, program başlatan servis
│   ├── install_autostart.py  # Bilgisayar açılışına otomatik ekleme scripti
│   └── requirements.txt      # psutil, pillow, mss, websockets, qrcode
├── server/                   # Bulut Röle & Wake-on-WAN Sunucusu (FastAPI & WebSocket)
│   ├── main.py               # REST API, WebSocket kanalı, log ve zamanlayıcı motoru
│   ├── wol.py                # UDP Magic Packet üreteci
│   └── auth.py               # JWT ve 6 haneli güvenli eşleştirme anahtarı
├── firmware_esp32/           # 5VSB Standby Gücüyle Çalışan PCIe/Optokuplör IoT Yazılımı
├── docs/                     # Store Yayınlama Kılavuzları ve Yasal Belgeler
│   ├── APPLE_STORE_PUBLISHING.md
│   ├── GOOGLE_PLAY_PUBLISHING.md
│   └── PRIVACY_POLICY.md    # KVKK ve GDPR uyumlu Gizlilik Politikası
├── uygulama_onizleme.html     # iOS Liquid Glass İnteraktif Canlı Simülatör
└── android_onizleme.html      # Android Material You İnteraktif Canlı Simülatör
```

---

## ⚡ Hızlı Başlangıç Rehberi

### 1. Canlı Tasarım Önizlemeleri (Tarayıcınızda Açın)
Hiçbir şey kurmadan arayüzleri, canlı ekranı ve program başlatıcıyı hemen tarayıcınızda denemek için:
- **iOS Sürümü İçin**: [`uygulama_onizleme.html`](uygulama_onizleme.html) dosyasını tarayıcınızda açın.
- **Android Sürümü İçin**: [`android_onizleme.html`](android_onizleme.html) dosyasını tarayıcınızda açın.

### 2. Bulut Röle Sunucusunu Başlatma
Sunucuyu kendi bilgisayarınızda veya ücretsiz bir bulut sağlayıcıda (Render.com, Railway, VPS vb.) çalıştırın:
```bash
cd server
pip install -r requirements.txt
python main.py
```
Sunucu `http://0.0.0.0:8080` portunda ve `/ws` WebSocket ucuyla yayına başlar.

### 3. Bilgisayarda Masaüstü Ajanını Çalıştırma
Yöneteceğiniz bilgisayarda ajanı başlatın:
```bash
cd desktop_agent
pip install -r requirements.txt
python agent.py
```
Ajanın bilgisayar her açıldığında arka planda otomatik başlaması için:
```bash
python install_autostart.py
```

### 4. Mobil Uygulamayı Başlatma
```bash
cd mobile_app
flutter pub get
flutter run
```

---

## 📱 Mağaza Yayınlama Rehberleri

Uygulamanızı mağazalara yüklerken incelemeden sorunsuz geçmeniz için hazırlanan hazır rehberler:
- 🍏 [Apple App Store Yayınlama Rehberi](docs/APPLE_STORE_PUBLISHING.md)
- 🤖 [Google Play Store Yayınlama Rehberi](docs/GOOGLE_PLAY_PUBLISHING.md)
- ⚖️ [Gizlilik Politikası Metni](docs/PRIVACY_POLICY.md)

---

## 🚀 GitHub Deposuna Yükleme Komutları

Bu projeyi doğrudan GitHub deponuza (`https://github.com/il4pt/Remote-Desktop`) göndermek için:

```bash
cd "/home/emre/Masaüstü/remote open"

# Uzak depoyu bağla
git remote set-url origin https://github.com/il4pt/Remote-Desktop.git 2>/dev/null || git remote add origin https://github.com/il4pt/Remote-Desktop.git

# Ana dala gönder
git push -u origin main
```

---

## 📄 Lisans
Bu proje **MIT Lisansı** altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakabilirsiniz.
