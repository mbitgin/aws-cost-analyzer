import json
import urllib.request
from src.core.ports.notification import NotificationPort
from src.config import settings


class SlackAdapter(NotificationPort):

    def send_savings_report(self, total_suggestions: int, total_savings: float, recommendations: list) -> bool:
        # Slack Markdown formatında zengin içerikli kurumsal mesaj bloğu oluşturuyoruz
        slack_text = (
            f"💰 *CloudTrim FinOps Raporu Ayağınıza Geldi!* 💰\n"
            f"========================================\n"
            f"Bulut altyapınızda tarama tamamlandı ve tam *{total_suggestions} adet* kritik atıl kaynak bulundu.\n\n"
            f"🚀 *Bu Ay Kurtarabileceğiniz Toplam Para:* `${total_savings:.2f} USD`\n"
            f"========================================\n\n"
            f"*Öne Çıkan AI Optimizasyon Önerileri:*\n"
        )

        # İlk 3 öneriyi mesaja ekleyelim (Kanalı kirletmemek için)
        for rec in recommendations[:3]:
            slack_text += f"• *{rec.resource.resource_type.value}* ({rec.resource.resource_id}): {rec.action_item} -> *${rec.potential_monthly_savings:.2f}/ay tasarruf.*\n"

        slack_text += f"\n👉 Detaylı analizleri uygulamak ve sunucuları kapatmak için hemen CloudTrim paneline gidin."

        payload = {"text": slack_text}
        
        # Güvenli URL kontrolü ve Mock modu (Local testlerin tıkanmaması için)
        if settings.SLACK_WEBHOOK_URL == "mock" or not settings.SLACK_WEBHOOK_URL.startswith("http"):
            print(f"\n[MOCK SLACK BİLDİRİMİ] Gerçek bir Webhook adresi girilmediği için terminale basılıyor:\n{slack_text}\n")
            return True

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                settings.SLACK_WEBHOOK_URL, 
                data=data, 
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req) as response:
                return response.status == 200
        except Exception as e:
            print(f"Slack bildirimi gönderilirken beklenmedik hata oluştu: {str(e)}")
            return False