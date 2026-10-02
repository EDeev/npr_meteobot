# NPR MeteoBot

**Русский** · [English](README.en.md)

[![CI](https://github.com/EDeev/npr_meteobot/actions/workflows/ci.yml/badge.svg)](https://github.com/EDeev/npr_meteobot/actions/workflows/ci.yml)

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

## Лицензия

Школьный проект (2022). Код открыт для изучения, отдельной лицензии нет.

## Автор

**Деев Егор Викторович** — [GitHub](https://github.com/EDeev) · [Telegram](https://t.me/DeevEgor) · [egor@deev.space](mailto:egor@deev.space)

---

<div align="center">
  <sub>⭐ Если проект оказался полезным, поставьте звёздочку на GitHub!</sub>
  <p><sub>Сделано с ❤️ — <a href="https://deev.space">deev.space</a></sub></p>
</div>
