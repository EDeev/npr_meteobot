# NPR MeteoBot

**Русский** · [English](README.en.md)

[![CI](https://github.com/EDeev/npr_meteobot/actions/workflows/ci.yml/badge.svg)](https://github.com/EDeev/npr_meteobot/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/EDeev/npr_meteobot)](https://github.com/EDeev/npr_meteobot/releases)

Telegram-бот для школьников Норильского промышленного района: присылает актировки (отмену занятий
из-за мороза и ветра) для своей смены и района и показывает прогноз погоды.

**Статус:** школьный проект (2022), завершён, в архиве

**Стек:** Python 3.10 · aiogram 2 · SQLite · Selenium + BeautifulSoup (сайт администрации, Gismeteo) · pymorphy2

- Подписка на актировки по смене (1 или 2) и району: Норильск, Талнах, Оганер, Кайеркан
- Регулярная проверка сайта администрации и рассылка подписчикам
- Прогноз погоды на день и на 10 дней вперёд (данные Gismeteo)

## Запуск

```bash
pip install -r requirements.txt
BOT_TOKEN=токен_от_BotFather python bot.py
```

База `sub.db` создаётся при первом запуске из `schema.sql`. Для актировок нужен Chrome: сайт
администрации читается через Selenium.

**Docker:** `docker run -d -e BOT_TOKEN=токен -v meteobot-data:/data ghcr.io/edeev/npr_meteobot` (то же —
`git.deev.su/edeev/npr_meteobot`). Chromium для прогноза уже в образе, `sub.db` — в томе `/data`.

## Лицензия

Школьный проект (2022). Код открыт для изучения, отдельной лицензии нет.

## Автор

**Деев Егор Викторович** — [GitHub](https://github.com/EDeev) · [Telegram](https://t.me/DeevEgor) · [egor@deev.space](mailto:egor@deev.space)

---

<div align="center">
  <sub>⭐ Если проект оказался полезным, поставьте звёздочку на GitHub!</sub>
  <p><sub>Сделано с ❤️ — <a href="https://deev.space">deev.space</a></sub></p>
</div>
