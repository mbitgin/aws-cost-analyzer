# CloudTrim: Agentic AI & FinOps Automated Cost Optimizer 💰🛡️

CloudTrim, bulut altyapılarındaki (AWS) maliyet kaçaklarını, atıl kaynakları ve yapılandırma hatalarını gerçek zamanlı tespit eden, kural motoru (Rule Engine) ile çok modlu yapay zekayı (LLM) hibrit çalıştıran **B2B SaaS tabanlı bir otonom FinOps asistanıdır.**

Yüksek güvenlik protokollerine (Salt-Okunur Erişim) sadık kalarak bulut ortamını tarar, deterministik eşik değerlerine göre süzgeçten geçirir, mükerrer AI maliyetlerini önlemek için akıllı kalıcılık katmanında önbellekler (Caching) ve alınması gereken aksiyonları kurumsal iletişim kanallarına (Slack) anında raporlar.

---

## 🏗️ Mimari Yaklaşım & Prensipler

Proje, endüstri standardı olan **Hexagonal Architecture (Ports and Adapters)** ve **Domain-Driven Design (DDD)** prensiplerine uygun olarak geliştirilmiştir.

* **Dependency Inversion (SOLID - D):** İş mantığı (Core Domain), dış bileşenlerden (FastAPI, SQLAlchemy, Boto3, OpenAI) tamamen izole edilmiştir. Veri kaynağının veya AI modelinin değişmesi çekirdek sistemi etkilemez.
* **Single Responsibility (SOLID - S):** Veri modelleri bütünlüğü korur, servisler iş kurallarını işletir, adaptörler ise sadece dış dünya entegrasyonundan sorumludur.
* **Resilience (Kırılmazlık):** OpenAI kota aşımı (429) veya kimlik doğrulama hatalarında, AWS erişim kısıtlarında sistem çökmez; **Graceful Degradation** ve kural bazlı yerel **AI Fallback** mekanizmalarıyla HTTP 200 kararlılığında çalışmaya devam eder.

---

## 🛠️ Teknoloji Yığını (Tech Stack)

* **Language:** Python 3.11+ (Asenkron ve Veri Odaklı Mimari)
* **Web Framework:** FastAPI (Ultra düşük gecikme, Depends tabanlı IoC ve otomatik OpenAPI/Swagger)
* **Cloud SDK:** Boto3 (AWS EC2 & EBS Resource/Client Analitiği)
* **AI Engine:** OpenAI GPT-4o-mini API (Structured & Role-Based Prompting)
* **ORM / Database:** SQLAlchemy v2 (Data Mapper Pattern) & SQLite (PostgreSQL Ready)
* **DevOps / Security:** Docker (Multi-Stage Build, Non-Root `appuser` Isolation) & Docker Compose

---

## 📂 Proje Klasör Yapısı

```text
cloudtrim/
│
├── src/
│   ├── core/
│   │   ├── domain/        # Değiştirilemez (Immutable) Pydantic Modelleri
│   │   ├── ports/         # Arayüzler / Sözleşmeler (Soyut Sınıflar - ABC)
│   │   └── services/      # Çekirdek İş Mantığı ve Dinamik Kural Motoru
│   │
│   ├── adapters/          # Dış Entegrasyonlar (FastAPI, Boto3, OpenAI, Slack, DB)
│   ├── config.py          # Pydantic-Settings ile Fail-Fast Konfigürasyon Yönetimi
│   └── main.py            # Uygulama Giriş Noktası & Bağımlılık Enjeksiyon Merkezi (Composition Root)
│
├── Dockerfile             # Multi-Stage, Güvenli Production Imaj Tasarımı
├── docker-compose.yml     # Konteynerizasyon ve Kalıcı Disk (Volume) Yönetimi
├── .dockerignore          # İmaj Güvenliği ve Hafifliği İçin Filtre
├── .gitignore             # Git Güvenlik Filtresi (.env ve DB koruması)
└── requirements.txt       # Sabitlenmiş (Pinned) Production Bağımlılıkları


🚀 Kurulum ve Çalıştırma
1. Yerel Geliştirme Ortamı (Local Mode)
Projenin bağımlılıklarını yükleyin:
pip install -r requirements.txt


Kök dizinde bir .env dosyası oluşturun ve yapılandırın:
ENVIRONMENT=development
OPENAI_API_KEY=your_openai_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-1
SLACK_WEBHOOK_URL=mock

Uygulamayı başlatın:
uvicorn src.main:app --reload --app-dir .


👉 Tarayıcıdan interaktif dökümantasyona erişin: http://127.0.0.1:8000/docs

2. Konteyner Modu (Docker - Production Mode)
Docker Compose kullanarak sistemi yerel işletim sisteminden ve bağımlılıklardan tamamen izole, non-root güvenlik zırhıyla tek tıkla ayağa kaldırın:
docker compose up --build


👉 Konteyner içindeki canlı API'ye erişin: http://localhost:8000/docs

🛡️ Siber Güvenlik ve Maliyet Koruma Önlemleri
Read-Only Compliant: Sistem bulut üzerinde asla "Yazma/Değiştirme" yetkisi (IAM Write) istemez. Güvenlik bariyerini sıfıra indirerek kurumsal entegrasyonu kolaylaştırır.

Anti-IDOR: Üretilen her finansal öneri kriptografik olarak güvenli UUID4 şemasıyla mühürlenir, dışarıdan tahmin edilemez.

Maliyet Bariyeri (AI Caching): Keşfedilen bir atıl kaynak veritabanına yazıldıktan sonra, sonraki taramalarda OpenAI API'sine tekrar istek atılmaz; veri DB'den çekilerek şirket bütçesi korunur.

Container Non-Root: Docker imajı root yetkileriyle çalışmaz; 8888 UID'li appuser kullanıcısı ile izole edilerek olası sızma girişimlerinde tüm sunucunun ele geçirilmesi engellenir.