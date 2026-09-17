<p align="center">
  <img src="https://img.shields.io/badge/Remote--Desktop-v1.0.0-00F59B?style=for-the-badge&logo=power&logoColor=black" alt="Version">
  <img src="https://img.shields.io/badge/iOS-Liquid%20Glass%2018-00F59B?style=for-the-badge&logo=apple&logoColor=white" alt="iOS">
  <img src="https://img.shields.io/badge/Android-Material%20Design%203-80E9BA?style=for-the-badge&logo=android&logoColor=black" alt="Android">
  <img src="https://img.shields.io/badge/Backend-FastAPI%20%2B%20WebSocket-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="License">
</p>

<h1 align="center">⚡ RemotePower / Remote-Desktop</h1>

<p align="center">
  <b>A production-grade, store-ready cross-platform ecosystem to remotely wake up, monitor, stream, and control your PC from iOS and Android devices anywhere in the world.</b>
</p>

<p align="center">
  <a href="README.md">🇬🇧 <b>English</b></a> •
  <a href="README_TR.md">🇹🇷 <b>Türkçe</b></a>
</p>

---

## 📖 Overview

**Remote-Desktop** is a complete, enterprise-level remote power and control ecosystem designed for seamless publishing on **Apple App Store** and **Google Play Store**. 

Unlike traditional local Wake-on-LAN tools that only function within the same home Wi-Fi network, RemotePower connects your devices securely via a lightweight **Cloud Relay & WebSocket Broker**, enabling you to wake up, live stream, monitor hardware metrics, and launch programs on your computer even when you are thousands of miles away on cellular data.

---

## ✨ Key Features

- ⚡ **Worldwide Remote Power On (Wake-on-WAN)**:
  - Wakes up your sleeping or turned-off PC over the internet using authenticated cryptographic Magic Packets.
  - Optional ESP32 smart hardware trigger support for guaranteed 100% physical power button simulation on S5 state.
- 📺 **Live Remote Desktop Stream**:
  - High-performance, low-latency live desktop screen viewing directly from your mobile screen (1080p / 30 FPS).
  - Visual status indicator showing real-time window states when apps are launched.
- 🚀 **Remote Application Launcher**:
  - Launch your favorite desktop programs (Steam, Google Chrome, VS Code, Spotify, Discord, Terminal) with a single tap from your phone.
  - Safety interlock: Prevents launching commands when the target PC is offline.
- ⏱️ **Automation, Scheduler & Power Activity Log**:
  - Schedule recurring auto-power on/off timers (e.g. weekdays at 08:30 AM).
  - Built-in UDP Port 9 health check & network latency ping tester.
  - Granular, real-time power event audit logs with millisecond timestamps.
- 🛡️ **Enterprise Security & Biometrics**:
  - **Apple Face ID / Touch ID** verification on iOS.
  - **Android Biometric Fingerprint** prompt for every critical power action.
  - End-to-end tokenized authentication (JWT & ephemeral pairing keys).
- 🎨 **State-of-the-Art Design Systems**:
  - **iOS**: Apple visionOS / iOS 18 **Liquid Glass** aesthetic (ambient fluid light orbs, frosted glass depth, specular reflections, Dynamic Island).
  - **Android**: Google **Material You (Material Design 3)** with ergonomic tonal cards, organic shapes, and dark obsidian finishes.
  - **Select Menu Navigation**: Clean, uncluttered dropdown switcher for swift transitions between all 6 tabs.

---

## 🏗️ Architecture & Repository Structure

```text
Remote-Desktop/
├── mobile_app/               # Flutter Multi-Platform Client (iOS & Android)
│   ├── lib/                  # Dart source code (Liquid Glass & Material 3 UI)
│   │   ├── screens/          # Dashboard, Live Screen, App Launcher, Scheduler, Settings
│   │   ├── widgets/          # Neon Power Button, Liquid Metrics Card
│   │   └── services/         # Cloud API, WebSocket, Biometric Auth (LocalAuth)
│   ├── ios/                  # Apple App Store ready (Info.plist permissions, Podfile)
│   └── android/              # Google Play SDK 34 compliant (Manifest & Gradle)
├── desktop_agent/            # Background Daemon for Host PC (Windows/macOS/Linux)
│   ├── agent.py              # Reports metrics, captures screen, launches apps & executes power commands
│   ├── install_autostart.py  # Zero-config OS boot startup installer
│   └── requirements.txt      # psutil, pillow, mss, websockets, qrcode
├── server/                   # Cloud Relay & Wake-on-WAN Broker (FastAPI & WebSocket)
│   ├── main.py               # REST API, WebSocket pub/sub hub, logs & scheduler backend
│   ├── wol.py                # High-performance UDP Magic Packet constructor
│   └── auth.py               # JWT & 6-character secure pairing PIN engine
├── firmware_esp32/           # Standby 5V PCIe/Optocoupler IoT Switch Firmware
├── docs/                     # Store Publishing Guidelines & Legal Compliance
│   ├── APPLE_STORE_PUBLISHING.md
│   ├── GOOGLE_PLAY_PUBLISHING.md
│   └── PRIVACY_POLICY.md    # GDPR & KVKK compliant Privacy Policy
├── uygulama_onizleme.html     # Interactive iOS Liquid Glass Live Simulator
└── android_onizleme.html      # Interactive Android Material You Live Simulator
```

---

## ⚡ Quick Start Guide

### 1. Instant Interactive UI Previews
You can test the entire interface, live screen stream, and program launcher immediately inside your web browser without installing any SDKs:
- **iOS Liquid Glass Simulator**: Open [`uygulama_onizleme.html`](uygulama_onizleme.html) in your browser.
- **Android Material You Simulator**: Open [`android_onizleme.html`](android_onizleme.html) in your browser.

### 2. Setting Up the Cloud Relay Server
Deploy the server on any cloud host (Render.com, Railway, VPS, or Cloudflare Tunnels):
```bash
cd server
pip install -r requirements.txt
python main.py
```
The server will bind to `http://0.0.0.0:8080` with native WebSocket support at `/ws`.

### 3. Setting Up the Host PC Agent
Run the agent on the computer you want to control:
```bash
cd desktop_agent
pip install -r requirements.txt
python agent.py
```
To ensure the agent launches automatically upon computer startup:
```bash
python install_autostart.py
```

### 4. Running the Mobile App
```bash
cd mobile_app
flutter pub get
flutter run
```

---

## 📱 Publishing to Stores

Detailed, step-by-step submission checklists and compliance files are provided:
- 🍏 [Apple App Store Submission Guide](docs/APPLE_STORE_PUBLISHING.md)
- 🤖 [Google Play Store Submission Guide](docs/GOOGLE_PLAY_PUBLISHING.md)
- ⚖️ [Privacy Policy Template](docs/PRIVACY_POLICY.md)

---

## 🚀 GitHub Push Instructions

To sync this repository with your GitHub remote (`https://github.com/il4pt/Remote-Desktop`):

```bash
cd "/home/emre/Masaüstü/remote open"

# Set remote origin
git remote set-url origin https://github.com/il4pt/Remote-Desktop.git 2>/dev/null || git remote add origin https://github.com/il4pt/Remote-Desktop.git

# Push to main branch
git push -u origin main
```

---

## 📄 License
Distributed under the **MIT License**. See `LICENSE` for more information.
