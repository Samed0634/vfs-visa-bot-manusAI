# VFS Global Appointment Bot - Kurulum ve Kullanım Kılavuzu

## İçindekiler

1. [Giriş](#giriş)
2. [Sistem Gereksinimleri](#sistem-gereksinimleri)
3. [Kurulum](#kurulum)
4. [Konfigürasyon](#konfigürasyon)
5. [Kullanım](#kullanım)
6. [Sorun Giderme](#sorun-giderme)
7. [Güvenlik ve Yasal Uyarılar](#güvenlik-ve-yasal-uyarılar)

## Giriş

VFS Global Appointment Bot, VFS Global web sitesinde otomatik olarak vize randevusu arayan ve bulan bir Python uygulamasıdır. Bot, Cloudflare gibi bot koruma sistemlerini aşmak için gelişmiş teknikler kullanır ve kullanıcıya Telegram üzerinden bildirim gönderir.

### Temel Özellikler

- **Otomatik Randevu Arama**: Belirtilen tarih aralığında sürekli randevu arar
- **Cloudflare Bypass**: `undetected-chromedriver` ile bot korumasını aşar
- **Akıllı Davranış**: İnsan benzeri etkileşimler simüle eder
- **Bildirim Sistemi**: Telegram ile anlık bildirimler
- **Detaylı Loglama**: Tüm işlemler loglanır ve hata durumunda ekran görüntüsü alınır
- **Docker Desteği**: Kolay deployment için Docker container desteği

## Sistem Gereksinimleri

### Minimum Gereksinimler

- **İşletim Sistemi**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.7 veya üzeri
- **RAM**: 2GB (4GB önerilir)
- **Disk Alanı**: 1GB boş alan
- **İnternet**: Stabil internet bağlantısı

### Gerekli Yazılımlar

- **Google Chrome**: En güncel sürüm
- **Python**: 3.7+
- **pip**: Python paket yöneticisi
- **Git**: Proje klonlama için (isteğe bağlı)

## Kurulum

### 1. Projeyi İndirme

#### Git ile klonlama (önerilen):
```bash
git clone https://github.com/your-username/vfs-visa-bot.git
cd vfs-visa-bot
```

#### ZIP dosyası ile:
1. GitHub'dan ZIP dosyasını indirin
2. Dosyayı çıkarın
3. Terminal/Command Prompt ile klasöre gidin

### 2. Python Sanal Ortamı Oluşturma (Önerilen)

```bash
# Sanal ortam oluşturma
python -m venv vfs_bot_env

# Sanal ortamı aktifleştirme
# Windows:
vfs_bot_env\Scripts\activate
# macOS/Linux:
source vfs_bot_env/bin/activate
```

### 3. Gerekli Paketleri Yükleme

```bash
pip install -r requirements.txt
```

### 4. Google Chrome Kurulumu

#### Windows:
1. [Chrome indirme sayfası](https://www.google.com/chrome/)ndan indirin
2. Kurulum dosyasını çalıştırın

#### macOS:
```bash
# Homebrew ile
brew install --cask google-chrome
```

#### Ubuntu/Debian:
```bash
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt update
sudo apt install google-chrome-stable
```

## Konfigürasyon

### 1. Konfigürasyon Dosyası Oluşturma

```bash
cp .env.example .env
```

### 2. Temel Ayarları Yapma

`.env` dosyasını bir metin editörü ile açın ve aşağıdaki alanları doldurun:

#### Zorunlu Ayarlar

```env
# VFS Global Hesap Bilgileri
VFS_USERNAME=your_vfs_username
VFS_PASSWORD=your_vfs_password

# Vize Detayları
VISA_TYPE=Tourism
APPLICATION_CENTER=Ankara
```

#### Tarih ve Saat Tercihleri

```env
# Randevu Tarihi Aralığı
PREFERRED_DATE_START=2025-07-01
PREFERRED_DATE_END=2025-12-31

# Saat Aralığı
PREFERRED_TIME_START=09:00
PREFERRED_TIME_END=17:00
```

### 3. Telegram Bildirimleri (İsteğe Bağlı)

#### Telegram Bot Oluşturma:

1. [@BotFather](https://t.me/botfather) ile konuşma başlatın
2. `/newbot` komutunu gönderin
3. Bot için bir isim belirleyin (örn: "VFS Randevu Bot")
4. Bot için kullanıcı adı belirleyin (örn: "vfs_randevu_bot")
5. Aldığınız token'ı kaydedin

#### Chat ID Alma:

1. Oluşturduğunuz bota bir mesaj gönderin
2. Tarayıcıda şu adresi açın: `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. `<TOKEN>` yerine bot token'ınızı yazın
4. JSON çıktısında `"chat":{"id":123456789}` şeklindeki ID'yi bulun

#### .env dosyasına ekleme:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
ENABLE_NOTIFICATIONS=true
```

### 4. Gelişmiş Ayarlar

```env
# Bot Davranışı
CHECK_INTERVAL=300          # Kontrol aralığı (saniye)
MAX_RETRIES=3              # Maksimum deneme sayısı
RETRY_DELAY=10             # Yeniden deneme gecikmesi
HEADLESS_MODE=false        # Tarayıcıyı gizli modda çalıştır
SCREENSHOT_ON_ERROR=true   # Hata durumunda ekran görüntüsü al

# Loglama
LOG_LEVEL=INFO             # DEBUG, INFO, WARNING, ERROR
LOG_FILE=vfs_bot.log       # Log dosyası adı
```

## Kullanım

### 1. Temel Çalıştırma

```bash
python main.py
```

### 2. Arka Planda Çalıştırma

#### Linux/macOS:
```bash
nohup python main.py > bot.log 2>&1 &
```

#### Windows (PowerShell):
```powershell
Start-Process python -ArgumentList "main.py" -WindowStyle Hidden
```

### 3. Docker ile Çalıştırma

#### Docker Build:
```bash
docker build -t vfs-bot .
```

#### Docker Run:
```bash
docker run -d --name vfs-appointment-bot vfs-bot
```

#### Docker Compose:
```bash
docker-compose up -d
```

### 4. Botu Durdurma

#### Normal çalışma:
- `Ctrl+C` tuş kombinasyonu

#### Arka plan çalışması:
```bash
# Process ID bulma
ps aux | grep main.py

# Process'i durdurma
kill <PID>
```

#### Docker:
```bash
docker stop vfs-appointment-bot
```

## Sorun Giderme

### Yaygın Hatalar ve Çözümleri

#### 1. "Chrome driver not found" Hatası

**Çözüm:**
```bash
# Chrome'un yüklü olduğundan emin olun
google-chrome --version

# Gerekirse Chrome'u yeniden yükleyin
```

#### 2. "Login failed" Hatası

**Olası Nedenler:**
- Yanlış kullanıcı adı/şifre
- CAPTCHA gereksinimi
- Hesap geçici olarak kilitlenmiş

**Çözüm:**
1. Kullanıcı adı ve şifreyi kontrol edin
2. VFS Global'e manuel olarak giriş yapıp hesabın aktif olduğunu doğrulayın
3. CAPTCHA varsa `HEADLESS_MODE=false` yapın ve manuel müdahale edin

#### 3. "Cloudflare blocked" Hatası

**Çözüm:**
```env
# .env dosyasında
HEADLESS_MODE=false
CHECK_INTERVAL=600  # Daha uzun aralık
```

#### 4. "No appointments found" Sürekli Mesajı

**Normal Durum:** Bu mesaj randevu bulunmadığında görünür.

**Kontrol Edilecekler:**
- Tarih aralığının doğru olduğu
- Vize tipinin doğru seçildiği
- Başvuru merkezinin doğru olduğu

### Debug Modu

Detaylı hata ayıklama için:

```env
LOG_LEVEL=DEBUG
```

Bu mod ile:
- Tüm web elementleri loglanır
- Sayfa kaynak kodları kaydedilir
- Detaylı hata mesajları görüntülenir

### Log Dosyaları

Bot çalışırken oluşturulan dosyalar:

```
logs/
├── vfs_bot_20250611_143022.log    # Ana log dosyası
screenshots/
├── error_20250611_143045.png      # Hata ekran görüntüsü
├── error_20250611_143045.html     # Hata sayfa kaynağı
└── success_20250611_144012.png    # Başarı ekran görüntüsü
```

## Güvenlik ve Yasal Uyarılar

### Güvenlik

1. **Kimlik Bilgileri:**
   - `.env` dosyasını asla paylaşmayın
   - Git repository'sine `.env` dosyasını eklemeyin
   - Güçlü şifreler kullanın

2. **Sistem Güvenliği:**
   - Botu güvenilir ağlarda çalıştırın
   - Düzenli olarak güncellemeleri kontrol edin
   - Antivirüs yazılımı kullanın

### Yasal Uyarılar

1. **Kullanım Koşulları:**
   - VFS Global'in kullanım koşullarına uygun kullanın
   - Otomatik erişim kısıtlamalarına saygı gösterin
   - Aşırı sık isteklerden kaçının

2. **Sorumluluk:**
   - Bu yazılım eğitim amaçlıdır
   - Kullanıcı tüm sorumluluğu üstlenir
   - Yazılım geliştiricileri hiçbir sorumluluk kabul etmez

3. **Etik Kullanım:**
   - Sadece kendi randevularınız için kullanın
   - Ticari amaçlarla kullanmayın
   - Diğer kullanıcıların haklarına saygı gösterin

### Risk Faktörleri

1. **Hesap Engellenmesi:**
   - Çok sık kontrol yapmak hesabın geçici engellenmesine neden olabilir
   - `CHECK_INTERVAL` değerini 300 saniyeden az yapmayın

2. **CAPTCHA:**
   - Bot CAPTCHA ile karşılaştığında manuel müdahale gerekebilir
   - `HEADLESS_MODE=false` yaparak tarayıcıyı görünür hale getirin

3. **IP Engellenmesi:**
   - Aynı IP'den çok fazla istek gönderilirse engellenebilir
   - Gerekirse VPN kullanın

## Destek ve Katkı

### Destek Alma

1. **GitHub Issues:** Teknik sorunlar için
2. **Dokümantasyon:** Bu kılavuzu detaylı okuyun
3. **Log Dosyaları:** Sorun bildirirken log dosyalarını paylaşın

### Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun
3. Değişikliklerinizi commit edin
4. Pull request gönderin

### Geliştirme Ortamı

```bash
# Development dependencies
pip install -r requirements-dev.txt

# Code formatting
black .

# Linting
flake8 .

# Testing
pytest
```

Bu kılavuz, VFS Global Appointment Bot'u güvenli ve etkili bir şekilde kullanmanız için gerekli tüm bilgileri içermektedir. Herhangi bir sorunla karşılaştığınızda, önce bu kılavuzu kontrol edin ve gerekirse GitHub Issues üzerinden destek alın.

