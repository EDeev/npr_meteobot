-- Схема базы бота и служебные строки, которые он ожидает (подписчиков нет)
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, id_user VARCHAR (255) NOT NULL,
    rating INTEGER (4) NOT NULL DEFAULT (0), status BOOLEAN NOT NULL DEFAULT (False),
    send BOOLEAN NOT NULL DEFAULT (True), part INTEGER (1) NOT NULL, city INTEGER (1) NOT NULL);
CREATE TABLE IF NOT EXISTS parts (part INTEGER PRIMARY KEY AUTOINCREMENT, nor VARCHAR (3), tal VARCHAR (3),
    oga VARCHAR (3), kae VARCHAR (3));
CREATE TABLE IF NOT EXISTS weather (id STRING, "1" VARCHAR, "4" VARCHAR, "7" VARCHAR, "10" VARCHAR,
    "13" VARCHAR, "16" VARCHAR, "19" VARCHAR, "22" VARCHAR);
CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE NOT NULL, part INTEGER (2) NOT NULL,
    weath STRING);

INSERT INTO parts (part, nor, tal, oga, kae) VALUES (1, '11', '11', '11', '11'), (2, '11', '11', '11', '11');
INSERT INTO weather (id) VALUES (' '), ('tomorrow'), ('3-day'), ('4-day'), ('5-day'), ('6-day'), ('7-day'),
    ('8-day'), ('9-day'), ('10-day');
INSERT INTO data (id, date, part) VALUES (1, '2022-02-24', 1);
