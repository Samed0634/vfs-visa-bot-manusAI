import requests
import logging
from config import Config

class NotificationService:
    """Service for sending notifications"""
    
    def __init__(self):
        self.logger = logging.getLogger('VFS_Bot.Notification')
        self.telegram_enabled = (
            Config.ENABLE_NOTIFICATIONS and 
            Config.TELEGRAM_BOT_TOKEN and 
            Config.TELEGRAM_CHAT_ID
        )
    
    def send_telegram_message(self, message):
        """Send message via Telegram Bot API"""
        if not self.telegram_enabled:
            self.logger.debug("Telegram notifications disabled or not configured")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                'chat_id': Config.TELEGRAM_CHAT_ID,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            self.logger.info("Telegram notification sent successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send Telegram notification: {str(e)}")
            return False
    
    def send_success_notification(self, appointment_details):
        """Send success notification when appointment is booked"""
        message = f"""
🎉 <b>VFS Randevu Başarıyla Alındı!</b>

📅 <b>Tarih:</b> {appointment_details.get('date', 'Bilinmiyor')}
🕐 <b>Saat:</b> {appointment_details.get('time', 'Bilinmiyor')}
🏢 <b>Merkez:</b> {appointment_details.get('center', Config.APPLICATION_CENTER)}
📋 <b>Vize Tipi:</b> {appointment_details.get('visa_type', Config.VISA_TYPE)}

✅ Randevunuz başarıyla alınmıştır. Lütfen belirtilen tarih ve saatte başvuru merkezine gidiniz.
        """
        
        self.send_telegram_message(message.strip())
    
    def send_error_notification(self, error_message):
        """Send error notification"""
        message = f"""
❌ <b>VFS Bot Hatası</b>

🚨 <b>Hata:</b> {error_message}

Bot çalışmasında bir sorun oluştu. Lütfen logları kontrol ediniz.
        """
        
        self.send_telegram_message(message.strip())
    
    def send_no_appointment_notification(self, check_count):
        """Send notification when no appointments are available"""
        message = f"""
⏳ <b>VFS Randevu Kontrolü</b>

🔍 <b>Kontrol Sayısı:</b> {check_count}
📅 <b>Tarih Aralığı:</b> {Config.PREFERRED_DATE_START} - {Config.PREFERRED_DATE_END}
🏢 <b>Merkez:</b> {Config.APPLICATION_CENTER}

❌ Henüz uygun randevu bulunamadı. Bot aramaya devam ediyor...
        """
        
        # Only send this notification every 10 checks to avoid spam
        if check_count % 10 == 0:
            self.send_telegram_message(message.strip())
    
    def send_start_notification(self):
        """Send notification when bot starts"""
        message = f"""
🚀 <b>VFS Bot Başlatıldı</b>

🎯 <b>Hedef:</b> {Config.VISA_TYPE} vizesi randevusu
🏢 <b>Merkez:</b> {Config.APPLICATION_CENTER}
📅 <b>Tarih Aralığı:</b> {Config.PREFERRED_DATE_START} - {Config.PREFERRED_DATE_END}
⏰ <b>Kontrol Aralığı:</b> {Config.CHECK_INTERVAL} saniye

Bot randevu aramaya başladı...
        """
        
        self.send_telegram_message(message.strip())

