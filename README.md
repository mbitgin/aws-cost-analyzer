# CloudTrim: Agentic AI & FinOps Automated Cost Optimizer 💰🛡️

CloudTrim is a B2B SaaS platform designed to identify cloud cost leaks, idle resources, and configuration issues across AWS environments. By combining a deterministic Rule Engine with multimodal AI (LLMs), it delivers intelligent, actionable FinOps recommendations while maintaining a security-first architecture.

The platform operates using **read-only AWS IAM permissions**, continuously analyzes cloud resources, filters findings through predefined business rules, minimizes unnecessary AI requests with an intelligent caching layer, and instantly delivers optimization reports to enterprise communication platforms such as Slack.

---

# 🏗️ Architecture

CloudTrim follows **Hexagonal Architecture (Ports & Adapters)** together with **Domain-Driven Design (DDD)** principles to ensure maintainability, scalability, and clean separation of concerns.

### Key Design Principles

### Dependency Inversion (SOLID - D)

The business logic is completely isolated from external technologies such as FastAPI, SQLAlchemy, Boto3, OpenAI, and Slack. Infrastructure components can be replaced without affecting the core domain.

### Single Responsibility (SOLID - S)

Each layer has a single responsibility:

- Domain models preserve business consistency.
- Services implement business rules.
- Adapters handle communication with external systems.

### Resilience

The application is designed to remain operational under external failures.

If OpenAI API rate limits (429), authentication errors, or AWS permission issues occur, CloudTrim automatically falls back to its local rule engine instead of failing, ensuring graceful degradation and uninterrupted service.

---

# 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.11+ |
| Backend Framework | FastAPI |
| Cloud SDK | Boto3 |
| AI Engine | OpenAI GPT-4o-mini |
| ORM | SQLAlchemy 2 |
| Database | SQLite (PostgreSQL-ready) |
| Containerization | Docker & Docker Compose |

---

# 📂 Project Structure

```text
cloudtrim/
│
├── src/
│   ├── core/
│   │   ├── domain/        # Immutable Pydantic domain models
│   │   ├── ports/         # Abstract interfaces (Ports)
│   │   └── services/      # Business logic & Rule Engine
│   │
│   ├── adapters/          # FastAPI, AWS, OpenAI, Slack, Database
│   ├── config.py          # Pydantic Settings configuration
│   └── main.py            # Application entry point
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── requirements.txt
```

---

# 🚀 Getting Started

## 1. Local Development

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
ENVIRONMENT=development
OPENAI_API_KEY=your_openai_api_key
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
SLACK_WEBHOOK_URL=mock
```

Run the application:

```bash
uvicorn src.main:app --reload --app-dir .
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

## 2. Docker Deployment

Build and start the application:

```bash
docker compose up --build
```

Swagger documentation:

```
http://localhost:8000/docs
```

---

# 🔍 Features

- Detect idle EC2 instances
- Detect unattached EBS volumes
- Rule-based cloud resource analysis
- AI-powered optimization recommendations
- Slack notification integration
- Intelligent caching to reduce AI costs
- Read-only AWS IAM integration
- REST API with OpenAPI documentation
- Dockerized deployment
- Modular Hexagonal Architecture

---

# 🔐 Security

### Read-Only AWS Access

CloudTrim never requires write permissions on AWS resources. The application only requests read-only IAM permissions, reducing security risks and simplifying enterprise adoption.

### UUID-Based Resource Tracking

Each optimization recommendation is assigned a cryptographically secure UUIDv4 identifier, preventing predictable resource enumeration.

### AI Cost Optimization

Previously analyzed resources are cached in the database. If the same resource is scanned again, CloudTrim retrieves the cached recommendation instead of making another OpenAI API request, significantly reducing operational costs.

### Non-Root Containers

Docker containers run as a dedicated non-root user (`appuser`, UID 8888), minimizing the impact of potential container compromise.

---

# 📈 Future Roadmap

- Multi-cloud support (Azure & Google Cloud)
- Kubernetes integration
- FinOps dashboard
- Cost forecasting with machine learning
- Scheduled automated scans
- Multi-tenant architecture
- Email and Microsoft Teams notifications
- Terraform integration

---

# 🤝 Contributing

Contributions are welcome.

If you would like to improve CloudTrim, feel free to fork the repository, open an issue, or submit a pull request.

---

# 📄 License

This project is licensed under the MIT License.



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
