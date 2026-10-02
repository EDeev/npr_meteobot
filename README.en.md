# NPR MeteoBot

[Русский](README.md) · **English**

[![CI](https://github.com/EDeev/npr_meteobot/actions/workflows/ci.yml/badge.svg)](https://github.com/EDeev/npr_meteobot/actions/workflows/ci.yml)

A Telegram bot for schoolchildren in the Norilsk industrial area: it sends class cancellations due to frost
and wind ("aktirovka") for the user's shift and district and shows the weather forecast.

**Status:** school project (2022), completed, archived

**Stack:** Python 3.10 · aiogram 2 · SQLite · Selenium + BeautifulSoup (city administration site, Gismeteo) · pymorphy2

- Subscription to cancellations by shift (1 or 2) and district: Norilsk, Talnakh, Oganer, Kayerkan
- Regular checks of the administration site and broadcasts to subscribers
- Weather forecast for the day and up to 10 days ahead (Gismeteo data)

## Running

```bash
pip install -r requirements.txt
BOT_TOKEN=token_from_BotFather python bot.py
```

The `sub.db` database is created on first run from `schema.sql`. Cancellations need Chrome: the
administration site is read with Selenium.

## License

School project (2022). The code is open for study; there is no separate license.

## Author

**Egor Deev** — [GitHub](https://github.com/EDeev) · [Telegram](https://t.me/DeevEgor) · [egor@deev.space](mailto:egor@deev.space)

---

<div align="center">
  <sub>⭐ If you find this project useful, give it a star on GitHub!</sub>
  <p><sub>Made with ❤️ — <a href="https://deev.space">deev.space</a></sub></p>
</div>
