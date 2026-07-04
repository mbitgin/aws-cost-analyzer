# 1. Aşama: Bağımlılıkların sanal ortama (venv) kurulması
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Bağımlılıkları /opt/venv dizininde izole bir sanal ortama kuruyoruz
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# 2. Aşama: Ultra-clean Production İmajı
FROM python:3.11-slim AS runner

WORKDIR /app

# Sadece builder aşamasında oluşturulan temiz sanal ortamı kopyalıyoruz
COPY --from=builder /opt/venv /opt/venv
COPY src/ ./src/

# Container içindeki Python'ın bu sanal ortamı kullanmasını sağlıyoruz
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=.

# Güvenlik Protokolü: Uygulamayı non-root çalıştırma
RUN useradd -u 8888 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["/opt/venv/bin/uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]