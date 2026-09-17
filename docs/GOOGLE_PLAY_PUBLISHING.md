# Google Play Store Yayınlama Rehberi (Android)

RemotePower uygulamasını Google Play Store'da yayınlamak için gereken adımlar:

---

## 1. Gereksinimler
1. **Google Play Console Hesabı**: [play.google.com/console](https://play.google.com/console) üzerinden tek seferlik geliştirici kaydı ($25).
2. **Hedef API Seviyesi**: Projemiz `targetSdkVersion 34` (Android 14) olarak yapılandırılmıştır, Google Play'in zorunlu şartını eksiksiz karşılar.

---

## 2. Release İmzası (Keystore) Oluşturma

Terminalde release imzası oluşturun:
```bash
keytool -genkey -v -keystore remote-power-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias remotepower
```

Bu anahtarı güvenli bir yerde saklayın (kaybedilirse güncelleme yüklenemez).

---

## 3. Android App Bundle (.aab) Derleme

Google Play artık `.apk` yerine `.aab` (Android App Bundle) formatını zorunlu tutmaktadır:

```bash
cd mobile_app
flutter clean
flutter pub get
flutter build appbundle --release
```

Derlenen paket:
`mobile_app/build/app/outputs/bundle/release/app-release.aab`
adresinde oluşacaktır.

---

## 4. Google Play Console Yükleme Adımları

1. Play Console'da **"Uygulama Oluştur"** deyin (Adı: RemotePower, Dil: Türkçe, Tür: Uygulama, Ücretsiz/Ücretli).
2. **Uygulama İçeriği** sekmesindeki zorunlu anketleri doldurun:
   - **Gizlilik Politikası**: `docs/PRIVACY_POLICY.md` metnini bir linke (örneğin ücretsiz GitHub Pages veya Notion) koyup URL'sini yapıştırın.
   - **Hedef Kitle**: 13 yaş ve üzeri.
   - **Reklam Durumu**: "Uygulamamda reklam yok".
3. **Yeni Sürüm Oluştur** diyerek `app-release.aab` dosyasını yükleyin.
4. Bireysel hesaplarda Google'ın zorunlu tuttuğu 14 günlük kapalı test (Closed Testing) sürecini 12 arkadaşınızın e-postasıyla başlatın ve ardından üretim (Production) incelemesine gönderin.
