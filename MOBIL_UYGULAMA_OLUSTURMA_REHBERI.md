# 📱 ASLANOĞLU KUYUMCULUK - MOBİL UYGULAMA OLUŞTURMA REHBERİ

## 🎯 İÇİNDEKİLER
1. [Android APK Oluşturma](#android-apk)
2. [iOS IPA Oluşturma](#ios-ipa)
3. [Sorun Giderme](#sorun-giderme)

---

# 🤖 ANDROID APK OLUŞTURMA

## ADIM 1: GEREKLİ YAZILIMLAR

### 1.1 Node.js & Yarn Kur
```bash
# Node.js 18+ gerekli
node --version  # 18.0.0 veya üzeri olmalı
yarn --version  # 1.22.0 veya üzeri olmalı
```

**İndirme Linkleri:**
- Node.js: https://nodejs.org/en/download/
- Yarn: `npm install -g yarn`

### 1.2 Java JDK 17 Kur

**Windows:**
1. https://www.oracle.com/java/technologies/downloads/#java17
2. "Windows x64 Installer" indir ve kur
3. `JAVA_HOME` environment variable ayarla:
   - "System Properties" → "Environment Variables"
   - Yeni: `JAVA_HOME` = `C:\Program Files\Java\jdk-17`
   - `Path` değişkenine ekle: `%JAVA_HOME%\bin`

**Mac:**
```bash
brew install openjdk@17
```

**Test Et:**
```bash
java -version  # 17.0.x görmeli
```

### 1.3 Android Studio Kur

1. **İndir:** https://developer.android.com/studio
2. **Kur:** Tüm varsayılan seçeneklerle
3. **SDK Ayarları:**
   - Android Studio aç
   - "Configure" → "SDK Manager"
   - SDK Platforms:
     - ✅ Android 13.0 (API 33)
     - ✅ Android 12.0 (API 31)
   - SDK Tools:
     - ✅ Android SDK Build-Tools 33.0.0
     - ✅ Android SDK Platform-Tools
     - ✅ Android Emulator

4. **Environment Variables (Windows):**
   - `ANDROID_HOME` = `C:\Users\[KullanıcıAdı]\AppData\Local\Android\Sdk`
   - `Path`'e ekle: `%ANDROID_HOME%\platform-tools`

**Test Et:**
```bash
adb --version  # Android Debug Bridge çalışmalı
```

---

## ADIM 2: PROJEYİ HAZIRLA

### 2.1 Proje Klasörüne Git
```bash
cd /path/to/altinv2/frontend
```

### 2.2 Dependencies Kur
```bash
yarn install
```

### 2.3 Backend URL Ayarla

**ÖNEMLİ:** APK'nız gerçek backend'e bağlanmalı!

`frontend/.env.production` dosyasını düzenle:

```env
# UYARI: APK için mutlaka production URL kullan!
REACT_APP_BACKEND_URL=https://doubtful-loise-altinv2-8d1bec5d.koyeb.app/api

# Veya kendi backend'iniz:
# REACT_APP_BACKEND_URL=https://your-backend.com/api
```

⚠️ **DİKKAT:** `localhost` kullanmayın! Telefonda çalışmaz!

---

## ADIM 3: PRODUCTION BUILD

### 3.1 React Build Al
```bash
yarn build
```

**Beklenen Çıktı:**
```
Compiled successfully in 45.23s
File sizes after gzip:
  125.38 kB  build/static/js/main.abc123.js
```

### 3.2 Capacitor Sync
```bash
npx cap sync android
```

**Çıktı:**
```
✔ Copying web assets from build to android...
✔ Creating capacitor.config.json in android...
✔ copy android in 234.56ms
✔ Updating Android plugins...
✔ update android in 123.45ms
✔ Sync finished in 0.567s
```

---

## ADIM 4: ANDROID STUDIO İLE BUILD

### 4.1 Projeyi Aç
1. Android Studio'yu başlat
2. **File → Open**
3. `frontend/android` klasörünü seç
4. **Trust Project** tıkla
5. Gradle sync bekle (2-5 dakika)

### 4.2 Build Type Seç

**Test için Debug APK:**
- Hızlı build
- Herhangi bir telefona kurulabilir
- İmza gerekmez

**Yayın için Release APK:**
- Optimize edilmiş
- İmza (keystore) gerektirir
- Google Play Store için gerekli

---

## ADIM 5A: DEBUG APK BUILD (Test İçin)

### Yöntem 1: Android Studio GUI
1. **Build → Build Bundle(s) / APK(s) → Build APK(s)**
2. Build tamamlanınca (5-10 dakika):
3. "locate" tıkla → APK'yı bulur

**APK Konumu:**
```
frontend/android/app/build/outputs/apk/debug/app-debug.apk
```

### Yöntem 2: Terminal
```bash
cd frontend/android
./gradlew assembleDebug
```

Windows:
```cmd
gradlew.bat assembleDebug
```

### Debug APK'yı Test Et

**Emulator'da:**
1. Android Studio → **Tools → AVD Manager**
2. "Create Virtual Device" → Pixel 4 seç
3. System Image: Android 13 (API 33)
4. Start
5. APK'yı drag & drop

**Gerçek Telefonda:**
1. Telefonda "Developer Options" aç
2. "USB Debugging" aktif et
3. USB ile bağla
4. Terminal:
```bash
adb devices  # Telefonunu görmelisin
adb install app-debug.apk
```

✅ **Test Checklist:**
- [ ] Splash screen görünüyor
- [ ] Logo ve "ASLANOĞLU Kuyumculuk"
- [ ] Ana sayfa yükleniyor
- [ ] Fiyatlar görünüyor
- [ ] Çevirici çalışıyor
- [ ] Dil değiştirme çalışıyor

---

## ADIM 5B: RELEASE APK BUILD (Google Play İçin)

### 5.1 Keystore Oluştur

**Windows:**
```cmd
cd frontend
keytool -genkey -v -keystore aslanoglu-release.keystore -alias aslanoglu-key -keyalg RSA -keysize 2048 -validity 10000
```

**Mac/Linux:**
```bash
cd frontend
keytool -genkey -v -keystore aslanoglu-release.keystore -alias aslanoglu-key -keyalg RSA -keysize 2048 -validity 10000
```

**Sorulan Bilgiler:**
```
Enter keystore password: [güçlü-şifre] (not al!)
Re-enter new password: [aynı şifre]
What is your first and last name? [İsim]
What is your name of your organizational unit? Aslanoğlu Kuyumculuk
What is the name of your organization? Aslanoğlu Kuyumculuk
What is the name of your City? [Şehir]
What is the name of your State? [İl]
What is the two-letter country code? TR
Is CN=..., OU=..., O=... correct? yes
Enter key password for <aslanoglu-key>: [Enter - aynı şifre kullan]
```

⚠️ **UYARI:** Bu keystore dosyasını KAYBET! Yedekle!
- Google Drive, Dropbox veya güvenli yere kopyala
- Şifreyi kaydet (uygulama güncellemelerinde gerekli)

### 5.2 Keystore'u Güvenli Yere Taşı

**Windows:**
```cmd
move aslanoglu-release.keystore C:\Users\[KullanıcıAdı]\Documents\
```

**Mac:**
```bash
mv aslanoglu-release.keystore ~/Documents/
```

### 5.3 Gradle Config Düzenle

`android/app/build.gradle` dosyasını aç ve şunu ekle:

**Windows path örneği:**
```gradle
android {
    ...
    
    signingConfigs {
        release {
            storeFile file('C:\\Users\\[KullanıcıAdı]\\Documents\\aslanoglu-release.keystore')
            storePassword 'güçlü-şifre'
            keyAlias 'aslanoglu-key'
            keyPassword 'güçlü-şifre'
        }
    }
    
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

**Mac path örneği:**
```gradle
storeFile file('/Users/[kullanıcı]/Documents/aslanoglu-release.keystore')
```

### 5.4 Release APK Build

```bash
cd frontend/android
./gradlew assembleRelease
```

Windows:
```cmd
gradlew.bat assembleRelease
```

**İlk build 10-15 dakika sürebilir!**

**APK Konumu:**
```
frontend/android/app/build/outputs/apk/release/app-release.apk
```

### 5.5 Release AAB Build (Google Play için)

```bash
./gradlew bundleRelease
```

**AAB Konumu:**
```
frontend/android/app/build/outputs/bundle/release/app-release.aab
```

Google Play Store AAB formatını tercih eder (daha optimize).

---

## ADIM 6: GOOGLE PLAY STORE'A YÜKLEME

### 6.1 Google Play Console Hesabı

1. https://play.google.com/console
2. $25 tek seferlik ödeme
3. Developer Agreement imzala

### 6.2 Yeni Uygulama Oluştur

1. "Create App"
2. **App name:** Aslanoğlu Kuyumculuk
3. **Default language:** Turkish
4. **App or game:** App
5. **Free or paid:** Free

### 6.3 Store Listing Doldur

**Kısa Açıklama (80 karakter):**
```
Canlı altın ve döviz fiyatları - Aslanoğlu Kuyumculuk
```

**Tam Açıklama:**
```
ASLANOĞLU KUYUMCULUK - Güncel Altın ve Döviz Fiyatları

📊 Özellikler:
• 14 altın ürünü canlı fiyatları
• 11 döviz kuru takibi
• Anlık Türkiye piyasası verileri
• Dönüştürücü özelliği
• TR/EN dil desteği
• Mobil optimize arayüz

Aslanoğlu Kuyumculuk ile altın ve döviz piyasasını takip etmek artık çok kolay!
```

### 6.4 Materyaller Upload

**Gerekli:**
- App icon: 512x512 PNG
- Feature graphic: 1024x500 PNG
- Screenshots: En az 2 (1080x1920 önerilir)
- Privacy policy URL

### 6.5 AAB Upload

1. **Release → Production**
2. "Create new release"
3. `app-release.aab` yükle
4. Release notes yaz:
```
İlk sürüm (1.0.0):
• Canlı altın ve döviz fiyatları
• Dönüştürücü özelliği
• TR/EN dil desteği
```
5. "Review release" → "Start rollout"

### 6.6 Review Süreci

- ⏱️ Süre: 1-7 gün (genellikle 2-3 gün)
- 📧 Email ile sonuç gelir
- ✅ Onaylanırsa: Yayında!

---

# 🍎 iOS IPA OLUŞTURMA

## ADIM 1: GEREKLİ YAZILIMLAR

### ⚠️ Gereksinimler:
- **macOS** (Windows'ta iOS build YAPILAMAZ!)
- **Xcode 14+**
- **Apple Developer Program** ($99/yıl)

### 1.1 Xcode Kur

1. Mac App Store'dan "Xcode" indir (15+ GB)
2. Kur ve aç
3. "Agree" terms
4. Command Line Tools kur:
```bash
xcode-select --install
```

### 1.2 Apple Developer Hesabı

1. https://developer.apple.com/programs/
2. $99/yıl ödeme yap
3. Developer Agreement kabul et

---

## ADIM 2: iOS PLATFORMU EKLE

### 2.1 Capacitor iOS Ekle

```bash
cd frontend
npx cap add ios
```

### 2.2 Sync Et

```bash
npx cap sync ios
```

---

## ADIM 3: XCODE'DA AÇ VE AYARLA

### 3.1 Xcode'da Aç

```bash
npx cap open ios
```

Veya manuel:
1. Xcode aç
2. **File → Open**
3. `frontend/ios/App/App.xcworkspace` seç

### 3.2 Signing & Capabilities

1. Sol panelde **App** seç (mavi ikon)
2. **Signing & Capabilities** tab
3. **Team:** Apple Developer hesabını seç
4. **Bundle Identifier:** `com.aslanoglu.kuyumculuk`
5. ✅ "Automatically manage signing"

### 3.3 Deployment Target

1. **General** tab
2. **Deployment Info**
3. **Minimum Deployments:** iOS 13.0

---

## ADIM 4: SIMULATOR'DA TEST

### 4.1 Simulator Seç

Xcode üst bar:
- **iPhone 14 Pro** seç (veya herhangi bir model)

### 4.2 Run

- ▶️ butonuna tıkla (veya Cmd+R)
- Simulator açılır ve uygulama yüklenir
- Test et:
  - Splash screen
  - Fiyatlar yükleniyor mu?
  - Çevirici çalışıyor mu?

---

## ADIM 5: GERÇEK CIHAZDA TEST

### 5.1 iPhone/iPad Bağla

1. USB ile Mac'e bağla
2. iPhone'da "Trust This Computer" onayla
3. Xcode'da cihazı seç (simulator yerine)

### 5.2 Provisioning Profile

İlk kez gerçek cihazda çalıştırırken:
1. Xcode otomatik olarak provisioning profile oluşturur
2. **Fix** butonuna tıkla
3. Apple ID girişi iste

### 5.3 Run

- ▶️ tıkla
- iPhone'da "Untrusted Developer" hatası çıkarsa:
  - Settings → General → VPN & Device Management
  - Developer App → Trust

---

## ADIM 6: ARCHIVE (IPA OLUŞTUR)

### 6.1 Release Scheme Seç

1. Xcode üst bar: **App → Edit Scheme**
2. **Run** seçili iken
3. **Build Configuration:** Release

### 6.2 Archive Oluştur

1. **Product → Archive**
2. 5-10 dakika sürer
3. Bitince "Archives" penceresi açılır

### 6.3 Distribute App

1. **Distribute App** tıkla
2. Seçenekler:
   - **App Store Connect:** Apple'a yükle (onay için)
   - **Ad Hoc:** Test için IPA (sınırlı cihazlar)
   - **Development:** Geliştirme cihazları

**App Store Connect için:**
3. "Upload" seç
4. Varsayılan seçeneklerle devam
5. Upload başlar (10-20 dakika)

---

## ADIM 7: APP STORE CONNECT

### 7.1 App Oluştur

1. https://appstoreconnect.apple.com
2. **My Apps → + → New App**
3. **Platforms:** iOS
4. **Name:** Aslanoğlu Kuyumculuk
5. **Primary Language:** Turkish
6. **Bundle ID:** com.aslanoglu.kuyumculuk
7. **SKU:** aslanoglu-kuyumculuk-001

### 7.2 App Information

1. **Category:** Finance
2. **Privacy Policy URL:** [URL]
3. **Support URL:** [URL]

### 7.3 Version 1.0

1. **Screenshots:**
   - iPhone 6.5": 1290x2796 (iPhone 14 Pro Max)
   - iPhone 5.5": 1242x2208 (iPhone 8 Plus)
   - En az 1 her boyutta

2. **Promotional Text:**
```
Canlı altın ve döviz fiyatları takibi
```

3. **Description:**
```
ASLANOĞLU KUYUMCULUK

📊 Özellikler:
• 14 altın ürünü canlı fiyatları
• 11 döviz kuru
• Dönüştürücü
• TR/EN dil desteği
```

4. **Keywords:**
```
altın,döviz,kur,fiyat,kuyumcu,gram,ons
```

5. **Support URL:** [website]
6. **Marketing URL:** [opsiyonel]

### 7.4 Build Seç

1. **Build** kısmında "+" tıkla
2. Upload ettiğin build'i seç (1.0)
3. **Export Compliance:** No encryption (sadece HTTPS)

### 7.5 Submit for Review

1. **Add for Review** tıkla
2. **Submit to App Review**
3. Review süreci: 1-3 gün

---

# 🔧 SORUN GİDERME

## Android Sorunları

### "SDK location not found"

**Çözüm:**
`android/local.properties` oluştur:
```properties
sdk.dir=C:\\Users\\[Kullanıcı]\\AppData\\Local\\Android\\Sdk
```

Mac:
```properties
sdk.dir=/Users/[kullanıcı]/Library/Android/sdk
```

### "Gradle sync failed"

```bash
cd android
./gradlew clean
./gradlew build --refresh-dependencies
```

### "App not installed"

1. Eski versiyonu kaldır
2. "Install from unknown sources" aktif et
3. Yeniden kur

### Beyaz Ekran

`.env.production` kontrol et:
```env
REACT_APP_BACKEND_URL=https://actual-backend-url.com/api
```

## iOS Sorunları

### "Signing for App requires a development team"

1. Xcode: **Signing & Capabilities**
2. **Team:** Apple Developer hesabını seç
3. **Automatically manage signing** işaretle

### "Provisioning profile doesn't support..."

1. **Clean Build Folder** (Cmd+Shift+K)
2. **Team** tekrar seç
3. Build tekrar

### Simulator çalışmıyor

```bash
xcrun simctl erase all
sudo killall -9 com.apple.CoreSimulator.CoreSimulatorService
```

---

# ✅ SON KONTROLLİST

## Android
- [ ] Backend URL production'a ayarlı
- [ ] yarn build başarılı
- [ ] npx cap sync android başarılı
- [ ] Debug APK test edildi
- [ ] Keystore oluşturuldu ve yedeklendi
- [ ] Release APK/AAB build edildi
- [ ] Google Play Console hazır

## iOS
- [ ] macOS + Xcode var
- [ ] Apple Developer hesabı ($99)
- [ ] npx cap sync ios başarılı
- [ ] Simulator'da test edildi
- [ ] Gerçek cihazda test edildi
- [ ] Archive oluşturuldu
- [ ] App Store Connect hazır

---

## 📞 DESTEK

Sorun yaşarsanız:
- GitHub: https://github.com/aberk4y/altinv2/issues
- Capacitor Docs: https://capacitorjs.com/docs

**Başarılar! 🚀**
