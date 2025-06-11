# VFS Global Appointment Bot

Otomatik olarak VFS Global web sitesinde vize randevusu arayan ve bulan bir Python botu.

## 🚀 Özellikler

- **Otomatik Randevu Arama**: Belirtilen tarih aralığında uygun randevuları otomatik olarak arar
- **Cloudflare Bypass**: `undetected-chromedriver` kullanarak bot korumasını aşar
- **Akıllı Bekleme**: İnsan benzeri davranış için rastgele bekleme süreleri
- **Bildirim Sistemi**: Telegram üzerinden anlık bildirimler
- **Hata Yönetimi**: Detaylı loglama ve hata durumunda ekran görüntüsü alma
- **Konfigürasyonlu**: `.env` dosyası ile kolay yapılandırma

## 📋 Gereksinimler

- Python 3.7+
- Google Chrome tarayıcısı
- VFS Global hesabı
- (İsteğe bağlı) Telegram Bot Token'ı

## 🛠️ Kurulum

1. **Projeyi klonlayın:**
```bash
git clone <repository-url>
cd vfs-visa-bot
```

2. **Gerekli paketleri yükleyin:**
```bash
pip install -r requirements.txt
```

3. **Konfigürasyon dosyasını oluşturun:**
```bash
cp .env.example .env
```

4. **`.env` dosyasını düzenleyin:**
```bash
nano .env
```

Gerekli alanları doldurun:
- `VFS_USERNAME`: VFS Global kullanıcı adınız
- `VFS_PASSWORD`: VFS Global şifreniz
- `VISA_TYPE`: Vize tipi (örn: Tourism, Business)
- `APPLICATION_CENTER`: Başvuru merkezi (örn: Ankara, Istanbul)
- `PREFERRED_DATE_START`: Tercih edilen başlangıç tarihi (YYYY-MM-DD)
- `PREFERRED_DATE_END`: Tercih edilen bitiş tarihi (YYYY-MM-DD)

## 🚀 Kullanım

### Temel Kullanım
```bash
python main.py
```

### Arka planda çalıştırma (Linux/macOS)
```bash
nohup python main.py > bot.log 2>&1 &
```

### Docker ile çalıştırma
```bash
docker build -t vfs-bot .
docker run -d --name vfs-bot vfs-bot
```

## ⚙️ Konfigürasyon

### Temel Ayarlar

| Parametre | Açıklama | Varsayılan |
|-----------|----------|------------|
| `VFS_USERNAME` | VFS Global kullanıcı adı | - |
| `VFS_PASSWORD` | VFS Global şifre | - |
| `VFS_BASE_URL` | VFS Global base URL | https://visa.vfsglobal.com/tur/tr/nld |
| `VISA_TYPE` | Vize tipi | Tourism |
| `APPLICATION_CENTER` | Başvuru merkezi | Ankara |

### Tarih ve Saat Ayarları

| Parametre | Açıklama | Varsayılan |
|-----------|----------|------------|
| `PREFERRED_DATE_START` | Tercih edilen başlangıç tarihi | 2025-07-01 |
| `PREFERRED_DATE_END` | Tercih edilen bitiş tarihi | 2025-12-31 |
| `PREFERRED_TIME_START` | Tercih edilen başlangıç saati | 09:00 |
| `PREFERRED_TIME_END` | Tercih edilen bitiş saati | 17:00 |

### Bot Ayarları

| Parametre | Açıklama | Varsayılan |
|-----------|----------|------------|
| `CHECK_INTERVAL` | Kontrol aralığı (saniye) | 300 |
| `MAX_RETRIES` | Maksimum deneme sayısı | 3 |
| `RETRY_DELAY` | Yeniden deneme gecikmesi (saniye) | 10 |
| `HEADLESS_MODE` | Tarayıcıyı gizli modda çalıştır | false |
| `SCREENSHOT_ON_ERROR` | Hata durumunda ekran görüntüsü al | true |

### Bildirim Ayarları

| Parametre | Açıklama | Varsayılan |
|-----------|----------|------------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token'ı | - |
| `TELEGRAM_CHAT_ID` | Telegram chat ID | - |
| `ENABLE_NOTIFICATIONS` | Bildirimleri etkinleştir | false |

## 📱 Telegram Bildirimleri

1. **Telegram Bot oluşturun:**
   - [@BotFather](https://t.me/botfather) ile konuşun
   - `/newbot` komutunu gönderin
   - Bot adı ve kullanıcı adı belirleyin
   - Aldığınız token'ı `.env` dosyasına ekleyin

2. **Chat ID'nizi alın:**
   - Botunuza bir mesaj gönderin
   - `https://api.telegram.org/bot<TOKEN>/getUpdates` adresini ziyaret edin
   - `chat.id` değerini `.env` dosyasına ekleyin

## 📊 Loglama

Bot tüm aktivitelerini loglar:
- **Konsol çıktısı**: Gerçek zamanlı durum bilgisi
- **Log dosyaları**: `logs/` dizininde detaylı loglar
- **Ekran görüntüleri**: `screenshots/` dizininde hata ve başarı görüntüleri

## 🔧 Sorun Giderme

### Yaygın Sorunlar

1. **"Chrome driver not found" hatası:**
   ```bash
   # Chrome'u yükleyin (Ubuntu/Debian)
   wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
   sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
   sudo apt update
   sudo apt install google-chrome-stable
   ```

2. **"Cloudflare blocked" hatası:**
   - `HEADLESS_MODE=false` yapın
   - Farklı bir IP adresi deneyin
   - Bekleme sürelerini artırın

3. **"Login failed" hatası:**
   - Kullanıcı adı ve şifrenizi kontrol edin
   - CAPTCHA manuel olarak çözülmesi gerekebilir
   - VFS Global hesabınızın aktif olduğundan emin olun

### Debug Modu

Detaylı loglama için:
```bash
export LOG_LEVEL=DEBUG
python main.py
```

## ⚠️ Önemli Notlar

- **Yasal Uyarı**: Bu bot eğitim amaçlıdır. VFS Global'in kullanım koşullarına uygun kullanın.
- **Güvenlik**: Kimlik bilgilerinizi güvenli tutun, `.env` dosyasını paylaşmayın.
- **Rate Limiting**: Çok sık kontrol yapmaktan kaçının, hesabınız engellenebilir.
- **CAPTCHA**: Manuel müdahale gerekebilir, botu izlemeye devam edin.

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🆘 Destek

Sorunlarınız için:
- GitHub Issues kullanın
- Detaylı log dosyalarını paylaşın
- Ekran görüntüleri ekleyin

## 🔄 Güncellemeler

- **v1.0.0**: İlk sürüm
  - Temel randevu arama ve alma
  - Telegram bildirimleri
  - Cloudflare bypass
  - Detaylı loglama

