#!/usr/bin/env python3
"""Вшитые настройки «Моста» (тот же формат, что custom.txt RustDesk): печатает base64 JSON.
Сервер и ключ берутся из переменных окружения MOST_HOST / MOST_KEY (секреты репозитория)."""
import base64, json, os

# открытый ключ нашего сервера (не секрет: сервер отдаёт его каждому, кто подключается)
SERVER_KEY = "XTeuCKFYbhRlyuHHPiJHVOQv0Eg257njFXs7kNHjt20="

host = os.environ["MOST_HOST"].strip()
key = os.environ.get("MOST_KEY", "").strip().strip('"').strip("'")
try:
    ok = len(base64.b64decode(key, validate=True)) == 32
except Exception:
    ok = False
if not ok:
    key = SERVER_KEY
cfg = {
    # внутреннее имя — только латиница (папка, служба, установка); для человека — «Мост» (MOST_DISPLAY_NAME при сборке)
    "app-name": "Most",
    # default-settings: начальные значения, пользователь может поменять
    "default-settings": {
        "view-style": "adaptive",          # картинка подгоняется под размер окна и экрана
        "show-monitors-toolbar": "Y",      # переключатель мониторов, если у удалённого ПК их несколько
        "lang": "ru",
    },
    # override-settings: свой сервер (пользователь не может его поменять) и скрытые разделы настроек.
    # Ключи hide-*/disable-* попадают во встроенные настройки (BUILTIN_SETTINGS) RustDesk.
    "override-settings": {
        "custom-rendezvous-server": host,
        "relay-server": host,
        "key": key,
        "api-server": "",
        "hide-server-settings": "Y",
        "hide-network-settings": "Y",
        "hide-proxy-settings": "Y",
        "hide-websocket-settings": "Y",
        "hide-security-settings": "Y",
        "hide-stop-service": "Y",
        "hide-help-cards": "Y",
        "hide-powered-by-me": "Y",
        "disable-change-id": "Y",
    },
}
print(base64.b64encode(json.dumps(cfg, ensure_ascii=True).encode()).decode())
