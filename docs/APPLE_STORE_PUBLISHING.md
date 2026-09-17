# Apple App Store Yayınlama Rehberi (iOS)

RemotePower uygulamasını Apple App Store'da sorunsuz yayınlamak için adım adım yönerge:

---

## 1. Gereksinimler
1. **Apple Developer Hesabı**: [developer.apple.com](https://developer.apple.com) üzerinden yıllık üyelik ($99/yıl).
2. **Mac Bilgisayar & Xcode**: macOS işletim sistemi ve en güncel Xcode sürümü.

---

## 2. İzinler ve Info.plist Uyumluluğu
Apple İnceleme Ekibi (App Store Review Guidelines), sebep belirtilmeden istenen izinleri doğrudan reddeder (Guideline 5.1.1).
Projenizdeki `ios/Runner/Info.plist` dosyasına aşağıdaki Türkçe ve kurumsal açıklamalar önceden eklenmiştir:

- `NSCameraUsageDescription`: "RemotePower, bilgisayarınızı telefonunuzla kolayca eşleştirmek amacıyla QR kodları taramak için kamera erişimi gerektirir."
- `NSFaceIDUsageDescription`: "RemotePower, bilgisayarınızın yetkisiz kişilerce açılıp kapatılmasını önlemek için Face ID ile biyometrik güvenlik sağlar."
- `NSLocalNetworkUsageDescription`: "RemotePower, aynı yerel ağda bulunan bilgisayarlarınıza Wake-on-LAN sihirli paketleri göndermek ve durumlarını tespit etmek için yerel ağ erişimine ihtiyaç duyar."

---

## 3. Derleme & App Store Connect'e Gönderim

Terminalde mobil uygulama dizinine gidin:
```bash
cd mobile_app
flutter clean
flutter pub get
flutter build ipa --release
```

Oluşan `.ipa` dosyası `build/ios/archive/Runner.xcarchive` yolunda olacaktır.
- Xcode'u açın -> **Window > Organizer** sekmesine gidin.
- Arşivi seçip **"Distribute App"** > **"App Store Connect"** adımlarını takip ederek yükleyin (veya Transporter uygulamasıyla sürükleyip bırakın).

---

## 4. App Store İnceleme Ekibini (Apple Review) Kolayca Geçme Taktikleri

> [!IMPORTANT]
> **Donanım / PC Test Tuzağı (Guideline 2.1)**:
> Apple inceleme uzmanları genellikle evinizdeki bilgisayara fiziksel olarak bağlanamaz. Uygulamanın incelenirken boş veya bozuk görünmemesi için:
> 1. **App Review Information** notlar kısmına bir adet Demo Sunucu veya açık test cihazı ekleyin.
> 2. Veya inceleme uzmanına: *"Bu uygulama, kullanıcının evinde veya ofisinde bulunan bilgisayarları Wake-on-LAN ve bulut ajanıyla açmasını sağlayan bir yardımcı araçtır. 'Manuel Wake-on-LAN' sekmesinden herhangi bir test IP ve MAC adresi girerek arayüzü ve paket gönderimini test edebilirsiniz."* açıklamasını ekleyin.
> 3. İnceleme için ekran görüntülerini ve bir adet 30 saniyelik ekran videosunu App Store Connect'e yükleyin.
