# Мост

Своя программа удалённого доступа на основе [RustDesk](https://github.com/rustdesk/rustdesk) (лицензия AGPL-3.0, код открыт).

Отличия от RustDesk:
- название «Мост» для человека (внутреннее имя `Most` — латиницей, его требует установщик), свой значок;
- адрес сервера и ключ вшиты при сборке (секреты `MOST_HOST`, `MOST_KEY`), настройки сети и безопасности скрыты;
- ссылки вида `most://connection/new/<ID>?password=…`.

Сборка: Actions → «Мост — сборка для Windows» → Run workflow. Готовый `most.exe` — в релизе `most-latest`.
Брендинг: `most/brand.py` (тексты, производитель), `most/config.py` (вшитые настройки), значки — `res/`, `flutter/assets/icon.*`.
