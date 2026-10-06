# Школьный Telegram-бот погоды и актировок Норильска (aiogram 2). pymorphy2 0.9 не работает на Python 3.11+
FROM python:3.10-slim
RUN apt-get update && apt-get install -y --no-install-recommends chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 \
    CHROME_BIN=/usr/bin/chromium CHROMEDRIVER=/usr/bin/chromedriver
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY *.py schema.sql ./
# база подписок sub.db создаётся в томе /data из schema.sql
VOLUME ["/data"]
WORKDIR /data
CMD ["python", "/app/bot.py"]
