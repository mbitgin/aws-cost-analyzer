import httpx
from openai import OpenAI
from src.core.ports.ai_service import AIServicePort
from src.config import settings


class OpenAIAdapter(AIServicePort):

    def __init__(self):
        api_key = settings.OPENAI_API_KEY

        # Çakışmayı önlemek için tamamen izole, sıfır konfigürasyonlu bir HTTP istemcisi oluşturuyoruz
        # Bu hamle, sistemden gelebilecek otomatik 'proxies' parametrelerini tamamen devre dışı bırakır.
        clean_http_client = httpx.Client(trust_env=False)

        # Temiz istemciyi OpenAI içine enjekte ediyoruz
        self._client = OpenAI(
            api_key=api_key,
            http_client=clean_http_client
        )

    def analyze_recommendation(self, resource_type: str, action: str, cost: float, savings: float) -> str:
        # Fallback (Yedekleme) Sistemi: Eğer anahtar mock ise veya boşsa
        if not self._client.api_key or "sk-proj-" not in self._client.api_key:
            return f"FinOps-Bot Analizi: Bu {resource_type} örneğinin düşük kullanımı tespit edilmiştir. İşlemi onaylayarak aylık ${savings:.2f} tasarruf sağlayabilir ve bütçenizi optimize edebilirsiniz."

        try:
            response = self._client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Sen kıdemli bir FinOps ve bulut maliyet optimizasyon uzmanı yapay zekasın. Sana verilen kaynak verilerine bakarak, neden kapatılması veya küçültülmesi gerektiğini kurumsal, profesyonel, net ve Türkçe olarak maksimum 2 cümle ile açıkla. Başına mutlaka 'FinOps-Bot Analizi: ' ifadesini ekle."
                    },
                    {
                        "role": "user",
                        "content": f"Kaynak Türü: {resource_type}, Aksiyon: {action}, Mevcut Maliyet: ${cost}, Kurtarılacak Para: ${savings}"
                    }
                ],
                max_tokens=150,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[OPENAI ADAPTER ERROR] API çağrısı sırasında hata: {str(e)}")
            return f"FinOps-Bot Analizi: {resource_type} altyapısının optimize edilmesiyle aylık bütçenizde ${savings:.2f} iyileştirme yapılabilir."